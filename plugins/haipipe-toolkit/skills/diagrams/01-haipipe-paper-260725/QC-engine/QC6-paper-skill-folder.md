# The paper skill folder: one folder per question asked, and ten named after the board

state: ✅ SETTLED · the shape is BUILT on disk and A4.1 ruled C on 260804: the families share a contract, not folder names
owner: JL
method: sort the folder by the question each skill answers, then name the delivery folders after the board groups they produce

## Opening

What should `skills/paper/` be sorted by?
`skills/paper/` is the folder holding the 37 shipped skills that write a paper, such as `haipipe-paper-draft`.
It is sorted today by a story: enter, then write, then ship, then respond.
The skills themselves answer three different questions, and only one of them is that story.
So a bucket named `3-deliver` holds fourteen skills, five of which deliver nothing.

**What the three questions are**: WHAT is delivered, HOW it gets made, and WHERE the paper's files live.
The first is the ten Delivery groups a paper board carries, from Opening through Round.
The second is the four phases every group runs, draft, probe, revise and check.
The third is the paper's own filesystem, which exists before any content does.

**What this page decides**: which of the three becomes the top folder, and what the other two become.
It also records the two defects the move forces into the open, and the one coupling that blocks it.

**Covered elsewhere**: `QC1` owns which route produces which delivery, and stays the map.
`QC2` owns what a stage contract must declare, and gains a rule if this lands.

## Diagram

**Three axes in one tree**: what the folder is sorted by today, against what the skills are actually about.

```text
  📖 SORTED BY A STORY, today            🧭 SORTED BY A QUESTION, proposed
  ───────────────────────────────        ─────────────────────────────────
  0-enter/      2 skills                 haipipe-paper/   🚪 the door
  1-lifecycle/  2                        container/       ⚙️ WHERE the files live
  2-phase/     13  ✅ one clean axis     phase/           ⚙️ HOW any group is made
  3-deliver/   14  ⚠️ three axes mixed   quality/         ⚙️ passes over any stage
  4-respond/    3  ⚠️ 3 for one job      route/           ⚙️ lifecycle · stage
  5-present/    2                        S01-opening/     📄 WHAT is delivered
  haipipe-paper/1                        S02-work/           one folder per
  venue/           the packs             …                   BOARD GROUP
                                         S10-round/
                                         venue/           🎯 per TARGET, untouched

  🔑 the rule a reader can hold: a folder named `SNN-*` is a delivery group.
     anything else is an axis. no punctuation needed to say it.
```

## Content

### 1 · The tree is sorted by a story, and the skills are not

**Where the story breaks**: the buckets that hold more than one kind of thing.

```text
  bucket        holds                                     really is
  ──────────────────────────────────────────────────────────────────────────
  2-phase/      draft · probe · revise · check       ✅  ONE axis, correct
  3-deliver/    project compile diffpdf overleaf word ✅  S9 Build, 5 of 14
                folder scaffold restructure conform  ⚠️  the CONTAINER axis
                claim-audit optimizer reviewer polish ⚠️  quality over any stage
  0-enter/      enter                                ✅  the door
                round                                ⚠️  S10 Round, a group
  4-respond/    haipipe-paper-rebuttal               ✅  the pipeline
                paper-rebuttal · rebuttal-response   ⚠️  2 pre-family duplicates
  5-present/    poster · slides                      ✅  S8 Present, misnamed
```

⚙️ Establishes that only one bucket holds a single axis, and names every place two or three are mixed.

#### 1.1 · `2-phase/` is the model, and it is the only one
(13 skills, four sub-buckets, nothing else in it)
Draft, probe, revise and check run inside every delivery group, so they live once and every group dispatches to them.
That is what an axis folder looks like when it holds exactly one question.
Nothing in this proposal changes it, and its name loses only its ordinal.

#### 1.2 · `3-deliver/` is three folders wearing one name
(5 skills deliver, 4 build the container, 4 audit any stage)
`haipipe-paper-project` projects approved board pages into LaTeX candidates, which is the heart of Build.
`haipipe-paper-scaffold` adds the LaTeX toolchain to a paper folder, which happens before a word is drafted and is filed in the last bucket.
`haipipe-paper-claim-audit` and `haipipe-paper-reviewer` read any stage's output, so they belong to no single group.

#### 1.3 · A group with no folder cannot show that it has no skill
(Literature has neither, and nothing on disk says so)
Eight stage contracts exist and they cover five of the board's ten groups.
Present, Build and Round are produced by skills that are not stages, and Literature is produced by nothing at all.
Today that fact lives in a sentence; under the proposed shape it is an empty directory a reader meets by typing `ls`.

### 2 · What the proposed tree is, exactly

**The shape**: every folder answers one question, and ten of them are named after the board.

```text
  skills/paper/
  ├── haipipe-paper/       🚪 the door, unchanged
  │
  ├── container/           ⚙️ folder · scaffold · restructure · conform
  ├── phase/               ⚙️ 0-draft · 1-probe · 2-revise · 3-check   (13, unchanged)
  ├── quality/             ⚙️ claim-audit · optimizer · reviewer · polish
  ├── route/               ⚙️ lifecycle · stage        RESOLVE, never own
  │
  ├── S01-opening/         📄 stage.md ×3   seed · venue · pitch
  ├── S02-work/            📄 stage.md ×3   resource · claims · narrative
  ├── S03-literature/      ❌ EMPTY, and that is the point
  ├── S04-value/           📄 the value binding half of draft-values
  ├── S05-display/         📄 stage.md ×1 + the four display renderers
  ├── S06-main/            📄 stage.md ×1   section-edit, main half
  ├── S07-appendix/        📄 stage.md ×1   section-edit, appendix half
  ├── S08-present/         📄 poster · slides
  ├── S09-build/           📄 project · compile · diffpdf · to-overleaf · to-word
  ├── S10-round/           📄 round · rebuttal
  └── venue/               🎯 one folder per TARGET, a different axis, untouched
```

🧭 Establishes the exact folder list, which axis each folder answers, and what moves into each of the ten group folders.

#### 2.1 · The lifecycle content comes out of the router
(8 pairs of `stage.md` and `template.md`, 22 files, 256 KB)
Every stage folder holds exactly two files, so the move is small and complete.
`haipipe-paper-stage` stops owning the contracts and resolves them instead, which is what its own contract already says it does.
`../../paper/haipipe-paper-stage/stages/index.yml` keeps the roster and its `dir:` values point into the `SNN-` folders.

#### 2.2 · The board's folder rule, copied exactly
(JL 260803, after checking what `_` already means in this repo)
`install.sh:143` prunes `_archive` and `_paper-writing-backup` by name, so a leading underscore already reads as "not shipped".
The naming instead copies the BOARD's own folder rule exactly, `QA-design` and `S01-opening`, so a group folder is spelled the same in the skills tree and in every paper.
The ordinal is padded because an unpadded S1, S10, S2 puts Round second in every listing, glob and tab-completion, and the group TOKEN is padded with it so the folder and the heading never disagree.

#### 2.3 · `venue/` does not move
(one folder per submission TARGET, which is neither a group nor a phase)
A venue pack is read by the `QBv` axis, and it already sits correctly outside the story buckets.
Moving it into a group folder would tie one journal to one delivery concern, and a venue cuts across all ten.

### 3 · Two defects the move forces into the open

**What the restructure exposes**: neither is created by it, and both are invisible today.

```text
  🔪 section-edit serves TWO groups, and its contract says so in prose
     board_family: "Main or Appendix, according to section_kind"
                    └── a SENTENCE where a family name belongs

  🕳 five of the ten groups have no stage at all
     s03_literature  ❌ no stage, no skill
     s04_value       ❌ no stage
     s08_present     ❌ no stage, 2 skills
     s09_build       ❌ no stage, 5 skills
     s10_round       ❌ no stage, 1 skill
```

🔪 Establishes the two facts the current tree hides, and neither is a consequence of moving folders.

#### 3.1 · One stage cannot declare two families
(`5-section-edit` writes both Main sections and Appendix letters)
`board_family` must resolve to one admitted family, and this one holds a sentence instead.
Splitting it into an `s06_main` half and an `s07_appendix` half lets each declare a real family and lets the checker resolve both.
That is worth doing on its own, before any folder moves, so the restructure lands on ground that already parses.

#### 3.2 · Empty is the honest state for five groups
(and a directory shows it where a table does not)
Eight stages were written for the groups that had one, and nobody ever claimed the other five were covered.
An empty `S03-literature/` is a finding a person meets without reading anything.
`QC1` then stops being an essay and becomes a listing, because every group points at a folder or at nothing.

### 4 · The coupling that blocks the move

**Why this page is OPEN**: `application/` was built from this exact skeleton on purpose.

```text
  skills/paper/            skills/application/
  ──────────────────       ──────────────────────
  0-enter/            ←→   0-enter/
  1-lifecycle/        ←→   1-lifecycle/
  2-phase/            ←→   2-phase/
  3-deliver/          ←→   3-deliver/
  4-respond/          ←→   4-iterate/
  venue/              ←→   venue/

  📄 application/SOP-paper-alignment.md exists to keep them in step:
     "round 1 gave application paper's SKELETON (spine, buckets, DPRC …)"
  ⚠️ 42 files across the toolkit name these bucket paths
```

⚠️ Establishes that the bucket names are a shared contract between two families, so moving one is a decision about both.

#### 4.1 · Restructuring paper alone breaks a symmetry somebody built deliberately
(the SOP's own words call the buckets a skeleton that was ported)
Application received these bucket names in a planned port, and a document exists whose whole job is keeping the two aligned.
Changing paper's tree without application's leaves that SOP describing a shape neither family has.
So the ruling this page needs is not about paper's folders; it is about whether the two families still share a skeleton.

#### 4.2 · Applications do not have ten delivery groups
(so `SNN-` cannot be ported the way the buckets were)
A paper's groups end in Main, Appendix, Build and Round, and an application's do not.
If the two families keep a shared skeleton, the group axis cannot be it, and paper would keep the buckets it has.
If they stop sharing one, each family sorts by its own board, which is the whole argument of `§1`.

## Aims

### A1 · ⚙️ The tree is sorted by a story, and the skills are not
- A1.1 · Every folder under `skills/paper/` answers exactly one question.
  **Done when:** no bucket holds skills from two axes, checked by listing each folder's members against the axis its name claims.

### A2 · 🧭 What the proposed tree is, exactly
- A2.1 · The ten delivery groups each have a folder named after the board group they produce.
  **Done when:** `skills/paper/s01_opening` through `s10_round` exist, and each holds the stage contracts and skills that write that group's pages.
- A2.2 · The lifecycle contracts live with their group rather than inside the router.
  **Done when:** each `stage.md` and `template.md` sits in its `SNN-` folder, `../../paper/haipipe-paper-stage/stages/index.yml` points at the new paths, and `../../paper/haipipe-paper-stage/check-contracts.py` still passes.

### A3 · 🔪 Two defects the move forces into the open
- A3.1 · One stage contract declares one family.
  **Done when:** `5-section-edit` is two contracts, each with a `board_family` that resolves, and the checker reports no deferral for either.

### A4 · ⚠️ The coupling that blocks the move
- A4.1 · The paper and application families either share a skeleton on purpose or stop sharing one on purpose.
  **Done when:** a ruling is recorded here, `../../application/SOP-paper-alignment.md` matches it, and no file has moved before that.

## States

### Decision Now

- [ ] 🗣 Does `skills/application` take the same shape: door + its OWN roster + workers, on the shared board?
      📍 JL 260805: "as long as we specify the Stages as S01 to S10, we can make a specific usage of haipipe-board. This will be the same to haipipe-application, right?" Yes, and the specials cost nothing now: S03/S04 load `for-literature`/`for-value`, display loads `for-display`, sections load `for-section`, all host-agnostic already. CORRECTED after reading the code (JL 260805: "no, it is not the same... they have their own style"): the application's roster is genuinely its own, read from `1-lifecycle/` on disk: the EVIDENCE LADDER 1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice is a refinement pipeline with sequential gates (no paper group chains like this); its VENUE is a GATE, not a stylist (the channel decides WHICH stages fire and how deep claims settle, needing a fires-per-venue contract field paper has no use for); and iterate's rounds are driven by deployment feedback, not reviewer letters. Shared for free: display, section-edit, and both evidence routes ride for-display, for-section, for-literature, for-value unchanged. The recipe is shared; the roster is not. Sequenced behind the paper's phase 1, running in the same tree.

- [x] 🗣 The thin paper: does `haipipe-paper-stage` fold into the door, and does `phase/` dissolve into flat workers?
      📍 Reopens this page as a new round (JL 260805: "maybe we can make it very thin"; then: stage "do we still need it?", phase "we don't need phase... or we want to immigrate"). The board family now owns all page logic (8 types, 4 phases, RUN), so what remains of stage is not an engine but a PACKET COMPILER: resolve the roster row, read stage.md, assemble the RUN packet, call board RUN.
      ⭐ `A ·` fold stage into `haipipe-paper` (one door, one router); retire the four phase HUBS; the seven LaTeX leaves (citation · values · display-req · place · results · evidence · proof) move to a flat `workers/` with no hubs, dispatched by each stage.md's declarations; humanizer moves to the writing family. The LaTeX leaves stay paper-side because the board engine never names a consumer family. ≈33 → ~17 skills, one router.
      `B ·` keep stage as its own thin skill (roster + packet only) and retire just the hubs.
      🛑 `Blocks` retiring any hub, and SEQUENCED behind one thing: RUN has not driven a live page yet; prove it once before the paper family bets its lifecycle on it.
      🤖 `If nobody answers` the hubs stay as thin overlays and nothing retires.
      ✅ `Ruled A` JL 260805: "please do A." Executed in two phases: phase 1 (mechanical, fresh-context agent) builds workers/, moves humanizer to writing, retires the draft/revise/check hubs and the three redundant routers to _old/, repoints references, and verifies with install + check-contracts + both board builds; the probe worker moves to workers/ INTACT because it carries real paper deltas (check-probe-cards.sh, the S03/S04 projection). Phase 2 (the door fold: stage + enter + lifecycle into haipipe-paper) needs merge judgment and runs next session, still sequenced behind one live RUN.

- [x] 🗣 Do the paper and application families still share one folder skeleton?
      RULED C, 260804 (JL: "ok, I agree, please go ahead and make them"). **The two families share a CONTRACT, not folder names.** The four phase rulebooks now live in the Board family, host-agnostic, and each family's worker loads them and adds only its own artifact knowledge. Application renames nothing.
      A · keep the shared skeleton. Paper keeps `0-enter … 4-respond`, and this page closes as REJECTED. The three axes stay mixed and `QC1` stays an essay.
      B · restructure paper only, and retire the shared-skeleton rule. Application keeps its buckets, `../../application/SOP-paper-alignment.md` is rewritten to say the families diverged, and paper gets `s01…s10`.
      C ✅ · the families stay symmetric in RULE rather than in folder names. What made this rulable was a measurement, not an argument: the two families each ship their own draft, probe, revise and check hub (1,263 lines against 531), and NONE of the eight loads `haipipe-board-page` at all, so each copied the page grammar from memory and each went stale on its own schedule. `haipipe-paper-draft` still named `## Items to Finish` five times, a section renamed that morning.
      → CC had recommended B on 260803. B was wrong for a reason `§4.2` half-saw: it treated the shared thing as the FOLDER NAMES, when the shared thing worth keeping was the four-phase loop. C keeps that and drops the names, so neither family pays a rename.

### A1 · ⚙️ The tree is sorted by a story, and the skills are not
- ⬜ A1.1 · Not started. Counted 260803: `3-deliver` holds 14 skills across three axes, `0-enter` holds a group page, and `4-respond` holds two pre-family duplicates.

### A2 · 🧭 What the proposed tree is, exactly
- ⬜ A2.1 · Not started, and blocked by A4.1. The shape is argued in `§2` and no file has moved.
- ⬜ A2.2 · Not started. Measured 260803: 8 stages, 22 files, 256 KB, each folder holding exactly `stage.md` and `template.md`.

### A3 · 🔪 Two defects the move forces into the open
- ⬜ A3.1 · Not started, and NOT blocked by A4.1. `5-section-edit`'s `board_family` is the string "Main or Appendix, according to section_kind", which no admitted family matches. This can be fixed before any folder moves.

### A4 · ⚠️ The coupling that blocks the move
- ✅ A4.1 · Ruled C on 260804: the two families share a CONTRACT, not folder names. Four host-agnostic phase rulebooks now ship under `board/page-phases/` as `haipipe-board-page-draft`, `-probe`, `-revise`, and `-check`, registered recursively by `install.sh --global` and resolving in the roster. Paper and application keep their family worker folders and load the shared Page Phase before applying artifact-specific rules.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `QC1-delivery-skill-map.md` · becomes a listing rather than an essay if this lands
- `QC2-stage-contract.md` · owns what a stage declares, and gains the resolve-to-a-live-page rule

📥 **Input files** · what the work reads

- `../../../paper/haipipe-paper-stage/stages/index.yml` · the stage roster and its `dir:` values
- `../../../paper/haipipe-paper-stage/check-contracts.py` · what would verify the move
- `../../../application/SOP-paper-alignment.md` · the document that keeps the two families in step
- `../../../../install.sh` · prunes `_`-prefixed folders, which is why the proposal uses none

## Law

- 🔑 **A folder named `SNN-<group>` is a delivery group; anything else is an axis.** It is the board's own rule, the one that spells `QA-design`, applied unchanged, so the skills tree and every paper's `0-lifecycle/` name a group the same way (JL 260803). The rule needs no punctuation to carry it, and a leading underscore must not be used, because `install.sh:143` already prunes `_archive` and `_paper-writing-backup` by name and the mark therefore reads as "not shipped".
- 🔢 **A group ordinal is zero-padded.** `S1, S10, S2` puts Round second in every listing, glob, tab-completion and in `install.sh`'s own `sorted()`.
- 🚫 **NOTHING MOVES BEFORE A4.1 IS RULED.** The bucket names are a shared contract with `application/`, named in 42 files, and one family cannot quietly leave it.
- 🎯 **`venue/` is not a group folder and never becomes one.** A venue cuts across all ten groups, so tying it to one is a category error.

## Log

260804 · A4.1 RULED C, and the ruling came from a measurement rather than an argument. The blocker had been stated as a folder-name coupling: `application/` was given paper's buckets in a planned port, 42 files name those paths, and a SOP exists to keep the two in step. What nobody had counted was what the two families actually duplicate. They each ship their own DRAFT, PROBE, REVISE and CHECK hub, 1,263 lines against 531, and NOT ONE of the eight loads `haipipe-board-page`; every one of them had copied the page grammar from memory, which is why `haipipe-paper-draft` still named `## Items to Finish` five times on the morning that section was renamed. So the thing worth sharing was never the bucket names, it was the four-phase loop, and B would have thrown away the valuable half to keep the worthless one. Built the same day: four host-agnostic phase contracts in the Board family, `-for-stage-draft`, `-for-probe-entry`, `-for-stage-revise`, `-for-stage-check`. PROBE is deliberately not named `-for-stage-probe`, because it is the one phase that writes a page it was not invoked on (the topic register plus a nested entry, both in another group), so it is contracted as a PAGE KIND instead. `install.sh --global` re-registered cleanly and all four resolve in the roster.
260803 · EXECUTED, on JL's "please update it to the new structure, and we can fix bugs later". The tree on disk is now the one `§2` draws: `container/` `phase/` `quality/` `route/` as the axis folders and `S01-opening/` through `S10-round/` as the groups, with `venue/` untouched. The eight stage contracts moved out of the router into their delivery group, so `index.yml`'s `dir:` values now point at `../../../S01-opening/seed` and its siblings. `install.sh --global` re-registered cleanly and all 37 `SKILL.md` files still resolve. Two things the move broke and fixed on the way: `check-contracts.py` was globbing `stages/*/`, so after the move it found ZERO contracts and still printed `form ok`, a checker passing because it looked at nothing, and it now follows `index.yml`; and two MISQ board pages cited the old bucket paths, now repointed. What did NOT happen is the A4.1 ruling: `application/` still carries the old skeleton and `SOP-paper-alignment.md` still describes a shape only one family has, so that Decision Now row stands and the two families have diverged in fact before diverging by ruling.
260803 · The naming aligned to the board rather than inventing one. The proposal first read `s01_opening/`, and JL asked for consistency with the paper board's own folders, which had just become `S01-opening/` beside `QA-design/` on every skill board. So the axis folders keep plain names, the group folders take `SNN-<group>`, and the zero-padding was pushed up into the group TOKEN as well: the headings are now `S01 · Delivery Opening` through `S10 · Delivery Round`, so a folder and its heading can never disagree and `S01.html` through `S10.html` sort in board order.
260803 · Opened after JL asked to rethink `skills/paper/`, and written before any file moved. The diagnosis is that the tree sorts by a story while the skills sort by three questions, which is why `3-deliver` holds fourteen skills and five of them deliver nothing. JL proposed the group axis as the top folder and asked whether the shared axes could drop the underscore; both are adopted, the second after checking that `install.sh` already prunes `_`-prefixed folders and that plain names sort correctly anyway. Pre-flight then found the blocker this page is OPEN on: `application/` was given these bucket names in a deliberate port and `../../application/SOP-paper-alignment.md` exists to keep the two families in step, so the move is a decision about two families rather than one. One correction along the way: `haipipe-paper-project` was read as project scaffolding and is actually projection, board pages into LaTeX candidates, so it belongs in Build and not in the container axis.
