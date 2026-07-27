# ⑦ The paper folder: what exists on disk
state: 🟡 PARTIAL
owner: JL
method: number the working machinery, leave the deliverable unnumbered, and create nothing before its unit exists

## Question
What is in one paper's folder, and how can a reader tell at a glance which parts are the manuscript and which are the machinery that produced it? A mature paper accumulates a board, a probe pool, generated LaTeX, display units, build scripts, archives and a compiled PDF, all in one directory. Without a rule that directory becomes a place where you check three things before daring to delete anything.

The rule is the prefix, and it is a test rather than a taste: `0-`, `1-` and `2-` mean working machinery, everything unnumbered is what a journal receives, and `rm -rf 0-* 1-* 2-*` must leave a paper that still compiles and still submits. A file that breaks the build when deleted has no business carrying a number.

The second rule is that nothing exists before it is needed. A new paper gets a control plane and one runnable page; every other page arrives when its unit is allocated, and the LaTeX toolchain arrives at the Display or section frontier and not before. What we want is a folder where every file present is a file somebody asked for, so an absence is information rather than an oversight.

## Boundary
- ✅ Covered here
  What a paper folder contains, the numbered and unnumbered split, what exists at creation versus later, and what crosses this folder's edges.
- ↪ Covered elsewhere
  What is on the board inside it is `QA7`; how a question leaves it is `QA5`; markdown versus tex authority is `QB2d`; who creates a page is `QA8`; what a display unit contains is `QC3` and `QD1`. What a STAGE is as an object, and what it takes to make one work, is the whole `QB` group, anchored at `QB1`; this face owns only which stages exist and which folder each one fills.

## Diagram
```
   A PAPER FOLDER.   the NUMBER is the delete test.
                     ● = exists on day 0   ○ = absent until allocated

   Paper-X/
   │
   ├─ ✂️ NUMBERED · working machinery ─────────────────────────────────┐
   │                                                                    │
   ● │  0-lifecycle/     ⑧ THE BOARD, and nothing but the board        │
   │ ● │    board.md · board.html                                       │
   │ ● │    0-seed/   ○ 1-work/   ○ 2-venue/    ○ 3-display/           │
   │ ○ │    4-main/   ○ 5-appendix/ ○ 6-submission/ ○ 7-round/         │
   │ ○ │    _archive/                                                   │
   │ │                                                                  │
   ● │  1-probes/        the near side of the wall            → ⑤       │
   │ ○ │    PPnn_<topic>/QXn_<slug>.md   topic-scoped, cross-stage      │
   │ │                                                                  │
   ○ │  2-src/           how the deliverable is BUILT, not what it is   │
   │   │    compile.sh · compile.ps1 · config.yaml · setup.sh           │
   │   └────────────────────────────────────────────────────────────────┘
   │
   └─ 📦 UNNUMBERED · THE DELIVERABLE ─────────────────────────────────┐
                                                                       │
     ○   <paper>.tex        the driver: \\input each section            │
     ○   <paper>.bib        HUMAN-ONLY. An agent greps; never writes.   │
     ○   <paper>.pdf        the compiled artifact                       │
     ○   sections/          GENERATED from ⑧'s 4-main pages. ONE WAY.   │
     ○   appendices/        GENERATED from ⑧'s 5-appendix pages         │
     ○   displays/          one folder per unit. THE ONLY home of an    │
     │                      asset. There is NO top-level figures/.      │
     ○   <venue>.cls · <venue>.bst      the venue shell                 │
                                                                       │
     └─────────────────────────────────────────────────────────────────┘

   ── the test the numbering encodes ────────────────────────────────
      rm -rf 0-* 1-* 2-*     and the paper still compiles and submits
```

```
   ── INSIDE ONE DISPLAY UNIT.  the delete test, one level down ─────

      displays/displayNN-<slug>/
        📦 float.tex      the \caption + \label the section \inputs
        📦 assets/        the promoted render: figure.pdf | table-body.tex
        ─────────────────────────────────────────────────────────────
        ✂️ README.md      what this display argues, and for which claim
        ✂️ preview.tex    a one-page standalone, to look at it alone
        ✂️ preview.pdf    the build product of that
        ✂️ source/        REBUILD.md, the script, the query
        ✂️ candidates/    renders we did not pick
        ✂️ versions/      renders we picked before

      2 of 8 ship. The unit is the ONE place the numbered/unnumbered
      split does not reach, because a unit is a folder, not a prefix.
      → the ruling that closes this is in Discussion, not yet made.

   ── ⚠️ why figures/ was WRONG, and is now gone ────────────────────
      It came from the npjDM2025 layout, which predates display units.
      On the MISQ paper figures/ holds 5 loose PNGs under ai_generated/
      and ZERO \includegraphics in the whole paper points at any of
      them. Every real graphic is already inside a unit's assets/.
      A second home for the same kind of thing is the exact defect
      this face forbids everywhere else.
```

```
   ── WHO WRITES WHAT, and WHICH SKILL THIS RULE CHANGED ────────────
      ✅ rewritten to this layout on 260726
      ⬜ still names paths that no longer exist   (old-path · STATUS.md)
      ➖ never names a paper path; nothing here to change

      WHAT ON DISK      WHO WRITES IT                 UPDATED?
      ─────────────────────────────────────────────────────────────
      Paper-X/          /haipipe-paper enter          ✅  0.5.0
      0-lifecycle/      haipipe-paper-folder          ✅  0.5.0
        board.md/html   /haipipe-board            ③   ➖  CALLED by ①,
                        never typed (QA4)                 not typed
        S-*.md          haipipe-paper-stage           ✅  0.7.0  8 contracts
      1-probes/         haipipe-paper-probe       ⑤   ✅  0.7.0
      2-src/            haipipe-paper-compile         ✅  0.2.0
      sections/         haipipe-paper-revise          ✅  0.2.0
      appendices/       haipipe-paper-revise           "
      displays/         haipipe-paper-stage           (the Display stage)
        assets/         a task or discovery run       ➖  across the wall
                        haipipe-paper-draft-display   ✅  0.2.0  finds only
      <paper>.tex       haipipe-paper-scaffold        ✅  0.2.0
      <paper>.bib       NOBODY. HUMAN-ONLY.           ➖  an agent greps
      <paper>.pdf       haipipe-paper-compile          "
      <venue>.cls/bst   the venue pack                ✅  90 templates
      whole tree        haipipe-paper-conform         ✅  0.2.0  THE test
                        haipipe-paper-restructure     ✅  0.2.0  migrates in
                        haipipe-paper-lifecycle       ✅  0.4.0  the router
                        haipipe-paper-diffpdf         ✅  0.2.0

      THE SPEC ITSELF   2-phase/REF/paper-folder-anatomy.md   ✅ rewritten
        its old "0- means manuscript source of truth" table said the
        OPPOSITE of the delete test. That table is why the family
        drifted; it is now the delete-test table.
```

```
   ── WHAT THE FOUR ✅ ARE, and why conform went first ───────────────

      conform 0.2.0       the delete test stopped being a convention
        the AUDITOR       and became block J of check_structure.sh:
                          resolve every \input · \includegraphics ·
                          \bibliography a master reaches, assert none
                          sits behind a number. Block D checks board
                          purity + one family one folder. 141 → 250 ln.

      folder 0.5.0        Board-first and minimal: README, .gitignore,
        DAY 0             0-lifecycle/ with board.md + ONE Seed page.
                          No STATUS.md. No 0-displays/. No empty tree.

      scaffold 0.2.0      reframed as THE MANUSCRIPT UPGRADE, not paper
        THE UPGRADE       creation. Its SIX TEMPLATES were rewritten,
                          not just its prose: driver, supplementary,
                          sections-README, wrapper, leaf, compile.sh.

      restructure 0.2.0   was migrating papers INTO the shape this rule
        THE MIGRATION     forbids, which made it the most harmful one
                          to leave stale. Now inverted, and the delete
                          test is a THIRD gate beside prose parity and
                          compile parity.

   ── conform first was deliberate ──────────────────────────────────
      It is READ-ONLY, so it could not break anything, and once it is
      correct it is the pass/fail test the other three are written
      against. Before it, nothing could tell you a folder was right,
      and the old version FAILED a folder that was.

      $ conform/scripts/check_structure.sh <paper>
      on the MISQ paper today:  exit 1 · 56 findings · 18 delete-test
```

```
   ── never created in advance ──────────────────────────────────────
      ✗ a request file · a Handoff sidecar · a generic section stub
      ✗ an empty stage tree · a page for a unit nobody has asked for

   ── the manuscript upgrade, at the Display or section frontier ────
      the venue shell, sections/, the .bib, the driver .tex and 2-src/
      arrive TOGETHER. A paper that never reaches Display never grows
      a LaTeX toolchain.
```

## Content
### The three numbered folders, and why only three
`0-lifecycle/` is the board, `1-probes/` is the evidence layer, `2-src/` is how the deliverable is built rather than what it is. Nothing else earns a number, because a number is a promise that the thing is deletable.

That promise is what the old layout could not make. `0-` meant two opposite things at once: `0-lifecycle/` was working state and `0-<paper>.tex` was the deliverable itself, so the prefix told a reader nothing, which is the only job a prefix has.

### One family, one folder
Inside `0-lifecycle/`, the folder name IS the S family name: SEVEN families, and eight folders. The mismatch is deliberate and is not yet resolved. `Round` was ruled a family on 260726 and the board tooling never learned it: `FAMILIES` in `haipipe-board/stage.py:25` is seven names, `resolve_filename("Round", …)` raises, and the live paper's `7-round/` holds only `_archive/` with zero `S-Round` pages. So the eighth folder exists and its family does not. Before 260726 the folders carried the old STAGE order and the two disagreed badly. `Work` was split across `1a-resource/` and `1b-claims/`, `Venue` across three, and `5-section-edit/` held Main, Appendix and Submission at once while Submission was also split with `6-submission/`. Nine folders, eight families, and not one clean mapping.

A reader can now place a page from its name alone: `S-Main-7-results.md` is in `4-main/`, and nothing else could be.

The eight families are not the eight stages, and the folders are named for the families. Which stage fills which folder, and what each one asks:
```
 STAGE            asks                                     ──▶ FAMILY      FOLDER
 0-seed           why might this paper exist?                  Seed 0      0-seed/
 1a-resource      does the evidence EXIST, and can it
                  CARRY a claim?                               Work 0      1-work/
 1b-claims        supported, weak, or GAP?                     Work 1        "
 2a-venue         which outlet, and what does it demand?       Venue 0     2-venue/
 2b-pitch         what is it selling, in one minute?           Venue 1       "
 3-narrative      how do claims become a manuscript arc?       Venue 2       "
 4-display        what figure or table carries each claim?     Display 0   3-display/
 5-section-edit   does each section's prose do its job?        Main <n>    4-main/
                                                               Appendix <A> 5-appendix/
 ──────────────────────────────────────────────────────────────────────────────────
 (no stage)                                                    Submission  6-submission/
 (no stage)     ⚠️ RULED a family 260726, NOT in FAMILIES     Round       7-round/
                    resolve_filename("Round", …) raises; 0 live pages
```
Three stages fill Venue, two fill Work, one fills either Main or Appendix depending on the section, and two families are filled by no stage at all. So the folder tree answers "where do I read this" and says nothing about what produced it. `QB2b` owns that seam; what a stage IS as an object is `QB1`.

A stage also declares whether it SURVIVES a change of journal, and that split is a fact about the stage set rather than about any one stage:
```
── venue_aligned:   free | aligned | venue_role ──────────────────
      TEST   could a different journal change this stage's ANSWER?

      venue-FREE                       survives a retarget untouched
      ┌──────────────────────────────────────────────┐
      │ 0-seed        why might this exist            │
      │ 1a-resource   does it exist, does it carry    │  THE SCIENCE
      │ 1b-claims     supported / weak / GAP          │
      └──────────────────────────────────────────────┘
                          │
                     2a-venue   ◄── THE PIN, `venue_role`,
                          │          neither free nor aligned
      ┌──────────────────────────────────────────────┐
      │ 2b-pitch      what it sells, to whom          │
      │ 3-narrative   reveal order, section list      │  THE TELLING
      │ 4-display     display budget, conventions     │
      │ 5-section-edit house style, citation density  │
      └──────────────────────────────────────────────┘
      venue-ALIGNED                      rewritten on retarget

      ⚖️ the line falls between what is TRUE and how it is TOLD.
         A claim's status does not change because a different editor
         reads it. A narrative's ORDER does.

   ── the case that hurts, and still lands aligned ──────────────────
      MISQ ──rejected──▶ another outlet
        evidence   KEPT         every claim, number and probe entry
        figures    MOSTLY LOST  limits and conventions differ
      expensive, and still right: a figure is an argument made FOR a
      venue, not a fact about the world.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      fields   runs · venue_aligned · unit · units · units_from
      reader   ③ THE EXECUTOR · an agent, reading prose        → QB1
      fails    🔇 SILENT. display declares `runs: once` over eleven
               independently gated units and nothing has ever raised.
      to bind  ✅ THIS ONE IS CHECKABLE, cheaply: a stage that declares
               `units:` must declare `runs: per-unit`. `4-display`
               declares the first and not the second, which is the whole
               defect, expressible as one assertion.
```
Evidence is venue-free. A retarget may rewrite how a paper is told and may not reopen what it found. What retargeting concretely does to each aligned stage has never been run end to end, so it is design rather than practice.

The set of stages is OPEN, and deliberately so. Adding one costs a row in `stages/index.yml`, a folder, and two files: no new skill, no version bump. Compiling, submitting and answering reviewers all sit outside the eight today and none of those exclusions was ever argued in writing, so if one should become a stage the argument is available rather than blocked. Rounds went the other way on 260726: made a family rather than a stage, which is why `7-round/` has pages and no contract.

The folder is also PURE. Every file in it is an S page or the board's own index, never a `.tex`, an asset or a scratch note. The moment something else lands there the board stops being a control plane and becomes a folder that happens to contain some pages.

### What crosses this folder's edge
```
 ① ──▶ ⑦   IN, and only through a stage run. The paper CONSUMES the
           settled contract and never stores a copy: no SKILL.md, no
           stage contract, no venue pack is ever copied in.

 ⑧ ──▶ ⑦   IN, by generation. 0-lifecycle/ is INSIDE this folder and is
           where the real Content lives. sections/ and appendices/ are
           produced FROM those pages. One direction, md to tex, never back.

 ⑦ ──▶ the wall   OUT. 1-probes/ holds one entry per question this paper
           cannot answer, bound BY PATH to a QA file in tasks/ or
           discoveries/. The paper asks; it never computes.

 ⑦ ──▶ ②   NOTHING. A paper never writes to a design board.
```
Almost nothing here is authored in place. The prose arrives from `⑧`, the numbers and citations across the wall, the LaTeX is generated. What this folder genuinely owns is the SHAPE: which containers exist, and which are allowed to be empty.

## Items to Finish
- [ ] 🗃 `.board-refs.bbl` is machinery sitting in the unnumbered half
      `refs.py` writes it into the paper root: the rendered bibliography a citation chip's panel prints, 62 KB on MISQ. It survives `rm -rf 0-* 1-* 2-*` and breaks nothing when deleted, which by this face's own test means it should carry a number, or live under `2-src/`. Dot-prefixed so face discovery skips it, and it should be in the paper's `.gitignore` either way. Filed 260726 rather than moved, because moving it means changing `refs.py` and writing a new path into a real paper folder.
- [x] 🌱 Choose a minimal scaffold
      A new paper receives no speculative LaTeX, no section stubs, and no page for a unit nobody has asked for.
- [x] 🧭 Make the scaffold Board-first
      `0-lifecycle/board.md` and one Seed page make a new paper runnable immediately.
- [x] 🔢 Number by deletability
      `0-` `1-` `2-` is working machinery, unnumbered is the deliverable, and `rm -rf 0-* 1-* 2-*` is the test (JL 260726).
- [x] 🗂 One family, one folder
      Seven S families with a folder each, plus `7-round/` whose family is declared and unimplemented; 40 pages migrated on the MISQ paper with none lost.
- [ ] 🔧 Make `Round` a family, or rule that it is not one
      It was ruled one on 260726 and `FAMILIES` in `haipipe-board/stage.py:25` still lists seven, so `resolve_filename("Round", …)` raises and `7-round/` cannot receive a named page. Either add it there and in `check-contracts.py:40`, or say rounds are a folder with a different naming rule and stop calling them a family.
- [x] 🖼 Delete `figures/` from the layout
      It predates display units. On the MISQ paper it holds 5 orphan PNGs that no `\includegraphics` in the paper points at, while every real graphic already sits in a unit's `assets/`. A second home for the same thing is the defect this face forbids elsewhere.
- [x] ✂️ The venue split is stated
      `PHILOSOPHY.md` and the per-stage `venue_aligned:` field, with `venue_role` for the pin itself.
- [ ] 📐 Define what retargeting does to each aligned stage
      Rewrite from scratch, or re-derive while keeping the argument. Different operations; the contracts do not distinguish them.
- [ ] 🧠 Rule whether a retarget reopens the claims stage
      It should not, by this design. Say so explicitly, because the temptation at a new venue is to re-cut the claims to fit.

- [ ] ✂️ Rule where a display unit's working half lives
      2 of a unit's 8 members ship: `float.tex` and `assets/`. `README.md`, `preview.tex`, `preview.pdf`, `source/`, `candidates/` and `versions/` never do, so `displays/` fails the delete test as it stands. See Discussion.
- [x] 🛠 Teach the four BUILD skills this layout
      Done 260726. `conform` 0.2.0 rewritten around the delete test as an executable check (block J) plus board purity (block D), and it now fails the MISQ paper with 56 findings. `folder` 0.5.0 scaffolds Board-first with one runnable Seed page and creates no `STATUS.md`. `scaffold` 0.2.0 reframed as the manuscript upgrade, with its six templates rewritten, not just its prose. `restructure` 0.2.0 migrates INTO the new shape and gained the delete test as a third non-negotiable gate.
- [x] 🧹 Align the remaining skills with this layout
      Done 260726, in four phases ordered by BINDING rather than by mention count. ① `haipipe-paper-stage` 0.7.0: eight `stages/*/stage.md` contracts, whose `artifact:`/`probes:`/`units:`/`output:` resolve at run time, so a stale one does not read wrong, it WRITES to the wrong place. ② `haipipe-paper-enter` 0.5.0, the console. ③ `haipipe-paper-lifecycle` 0.4.0, the router. ④ the tail: `probe` 0.7.0, `draft-display` 0.2.0, `diffpdf` 0.2.0, `compile` 0.2.0, `revise` 0.2.0.
      Two things the plan had not counted, both found by measuring directories instead of `SKILL.md`: `2-phase/REF/paper-folder-anatomy.md`, the shared spec every build skill cites, whose prefix table asserted the OPPOSITE rule and is the reason the family drifted; and 90 venue templates carrying one identical stale line.
- [x] 📍 Rule STATUS.md out of existence
      Adopted 260726 on JL's proposal, with the Gate Ledger landing in each S page's `## Log`, one row on the page whose gate it was. That was the only blocker: it is the one part of the file that is history and cannot be re-derived. `current_layer`/`maturity` are derived from disk; the `venue:` pin moved to `S-Venue-0-venue.md` frontmatter. `folder` no longer creates the file, `conform` warns when one exists, `restructure` migrates its rows out before removing it, and `DRIFT` was retired with it: it named the gap between a stored frontier and disk, and there is no stored frontier. What replaced it is narrower and real, `STALE`, an S page whose own `state:` over-claims about itself.
- [x] 🧨 Make the MISQ paper pass its own test
      Done 260726 with `restructure` 0.2.0. Block J now reads `✓ nothing the deliverable needs sits behind a number`, and the test was also run for real on a copy: `rm -rf 0-* 1-* 2-*` then a four-pass compile produces the PDF. All three gates passed: prose parity byte-identical once path-bearing lines are excluded, compile parity 42 pages to 42 pages, delete test green. 56 findings to 47, and the 18 delete-test failures to zero. What the other 47 are is in Where we are; none of them is this item.
- [ ] 🧪 Create one paper and enter it
      A fresh agent should open its Board and work Seed without adding or guessing another control file.

## Where we are
The layout is ruled, and exactly one folder has been built to it: `0-lifecycle/` on the MISQ paper, eight family folders holding 40 S pages relocated with every name preserved, and all Links and stage contracts repointed and verified.

The rule now also lives somewhere a machine can read it. The four `1-build/` skills were rewritten on 260726, and `haipipe-paper-conform` 0.2.0 turned the delete test from a convention into a check: block J resolves every `\input`, `\includegraphics` and `\bibliography` target a master reaches and asserts none sits behind a number. Run against the MISQ paper it exits 1 with 56 findings, 18 of them delete-test failures including the driver `.tex` and the `.bib`. Before, nothing could tell you whether a paper folder was correct, and `conform` would have failed a folder that was.

The rest of the family has now been told too. Twelve skills were aligned on 260726, ordered by binding rather than by mention count: the eight stage contracts first, then the console, the router, and the tail. With them went the two things a `SKILL.md`-only count had missed: `2-phase/REF/paper-folder-anatomy.md`, the shared spec every build skill cites, whose prefix table asserted the opposite rule and is the reason the family drifted at all; and 90 venue templates carrying one identical stale line.

And the paper has now been migrated too (260726, JL's go). The MISQ top level is three numbered folders and an unnumbered deliverable: the driver, the `.bib` and the `.pdf` lost their prefix; `0-sections/` split into `sections/` and `appendices/` by what the driver actually reaches; `0-displays/` became `displays/`; the build pair moved into `2-src/`; `figures/` and `0-extra/` went to `_archive/`; the empty `1-board/` is gone; `1-rounds/` moved to `0-lifecycle/7-round/_archive/`; and `STATUS.md` is deleted with all nine of its gate rows on the S pages whose gates they were.

`STATUS.md` closed on the way, which is why that ruling is now `[x]`. The Gate Ledger was the only blocker and it landed exactly where this page proposed: seed and the seed re-run on `S-Seed-0`, pitch on `S-Venue-1`, claims on `S-Work-1`, narrative on `S-Venue-2`, display on `S-Display-0`, and the three rows belonging to no single page on `S-Venue-3` alongside the Restart Note and the display-directory note. The 2026-07-20 `> CHECK` block travelled with them, intact, annotated as dissolved rather than answered: both horns of its question were about which stored frontier to trust, and there is no longer one.

Forty-seven findings remain and not one is a delete-test failure. They fall in three groups, each owned elsewhere. Four are legacy flat buckets inside `displays/`, `Table/` `Figure/` `AppendixTable/` `AppendixFigure/`, which the manuscript still `\input`s directly; unitizing them is not a rename, because the bucket file and its unit's `float.tex` differ in content, so it is a display-stage promotion and it would have broken prose parity here. Twenty are board-purity findings inside `0-lifecycle/`, the build products and per-section scaffold folders this page already records as blocked on `QB2b`. The rest are section-stage: leaf naming, seven orphan leaves nothing `\input`s, a numbering gap at 06 to 08, and three wrappers carrying prose.

One thing remains open and this page stays 🟡 until it closes: where a display unit's working half lives. That is the `✂️` item, and the migration made it sharper rather than softer, because `displays/` is now unnumbered and therefore inside the deliverable, so the six non-shipping members of every unit ship with it.

## Files
- `3-deliver/1-build/haipipe-paper-conform/scripts/check_structure.sh`
  THE machine test for this face. Blocks A to K; block J is the delete test, block D is board purity and one-family-one-folder. Exit 0 conforms, 1 findings, 2 not a paper folder.
- `3-deliver/1-build/`
  The other three: `haipipe-paper-folder` (Board-first minimal scaffold), `-scaffold` (the manuscript upgrade), `-restructure` (migrate an existing paper in). All four rewritten 260726.
- `0-enter/haipipe-paper-enter/SKILL.md`
  The entry path that creates and opens the initial board; 9 old-layout mentions, the second-worst.
- `1-lifecycle/haipipe-paper-lifecycle/SKILL.md`
  The router that names paths on the way through; 6 mentions.
- `README.md`
  The family map, which still describes the older complete-folder shape.

## Law
The NUMBER is the delete test. A `0-`, `1-` or `2-` prefix means working machinery; everything unnumbered is the deliverable. `rm -rf 0-* 1-* 2-*` must leave a paper that still compiles and still submits, and a file that breaks the build when deleted has no business carrying a number.

Three numbered folders, and only three: `0-lifecycle/` the board, `1-probes/` the evidence layer, `2-src/` how the deliverable is built. Generated prose lands unnumbered, in `sections/` and `appendices/`, because a journal receives it.

`displays/` is the ONLY home of an asset, one folder per unit. There is no top-level `figures/` and no `Figure/` or `Table/` bucket: a display is a unit, and its render lives inside it.

Inside `0-lifecycle/`, one family one folder, and the folder holds S pages and its own index and nothing else.

A new paper is created Board-first and minimal, and every other page is absent until its unit is allocated. No request file, sidecar, section stub or empty stage tree is created in advance. Manuscript machinery is an upgrade performed at the Display or section frontier, never at creation.

Every stage declares exactly one of venue-free or venue-aligned, decided by whether a different journal could change its answer. The venue stage itself declares `venue_role`, because it is the stage that picks the venue and is therefore neither. Evidence is venue-free: a retarget may rewrite how a paper is told and may not reopen what it found.

## Discussion
> JL 260726: things like 0, 1, 2 are the things we can delete when we want to submit.
> CC: adopted as the delete test, and it is checkable rather than a convention.

> CC 260726: one case does not fit and I have not resolved it. A display UNIT holds both halves, and the split is 2 of 8: `float.tex` and `assets/` ship; `README.md`, `preview.tex`, `preview.pdf`, `source/`, `candidates/` and `versions/` never do. Today they sit in one folder, so the delete test cannot be run on `displays/` without losing what a journal needs.
> Three ways out, none ruled: put the working six under `displays/<unit>/_work/`; or move them to `2-src/displays/<unit>/`; or accept the straddle and state that `displays/` is the one folder the test does not apply to. The first keeps a unit together and is what I would try first.

> JL 260726: we might not need STATUS.md and not need the status strip any more.
> CC: I agree on the file, and the case is stronger than a preference. Three arguments, in order of weight.
> ONE, the console already stopped reading it. `haipipe-paper-enter` describes itself as a derive-from-disk dashboard and says so explicitly at its own line 289: a strip glyph is "the strip's artifact-on-disk test, not a frontier claim". The stage strip was designed in the 260622 feedback around "single source of truth = STATUS.md `current_layer`" with the stated precondition that "a stale current_layer = a lying strip". That design has already been abandoned in place; the file is what is left of it.
> TWO, it is now the third answer to "where is this paper", after the S pages' `state:` and the disk. `QA7` forbids exactly that.
> THREE, the MISQ file is a live demonstration. It disagrees with itself in three directions at once: `current_layer: section-edit`, a Restart Note saying the frontier reset to `0-seed`, and a Gate Ledger showing five stages confirmed. It carries a 12-line CHECK note from 260720 asking a human to rule on its own self-contradiction. That note is not a bug in the file; it is what a stored frontier costs.
> The one thing genuinely NOT derivable is the Gate Ledger: who confirmed which gate, when, and why. History cannot be read off current disk state. It belongs in each S page's `## Log`, one row on the page whose gate it was, which is also where a reader is already standing when they want it.
> On the strip I would separate two things. Deleting the stored `current_layer` it was designed to read: yes, and it already does not read it. Deleting the strip itself: that is a different question about how a reply closes, not about this folder, and it belongs on `QA7` or `QA2` rather than here.

## Log
260726 · The MISQ paper migrated, on JL's go, and this face's last blocking item closed. Three gates, all green: prose parity byte-identical, compile parity 42 pages to 42, and the delete test run for real on a copy rather than only asserted by block J. Two defects surfaced by doing the work rather than by reading anything. `haipipe-paper-scaffold`'s `compile.sh.tpl` was rewritten for `2-src/` but still discovered its master with `ls 0-*.tex`, so the one script a migrated paper installs could never find that paper's driver: it now takes the unnumbered top-level `.tex` carrying `\documentclass`. And the block that does it crashed on macOS, because bash 3.2 mis-parses a `case` pattern's `)` inside a process substitution; it is a plain loop now. Two decisions were deliberately NOT taken here: the flat buckets under `displays/` are a content promotion rather than a rename, and the board-purity findings are `QB2b`'s.

260726 · Rounds moved inside the lifecycle as an eighth family, one page per round. Folders renumbered to one-family-one-folder; 40 pages migrated with none lost. Numbered-versus-unnumbered adopted as the delete test on JL's ask. Page then rewritten clean: three Content divisions instead of seven, with the scaffold, the absent-until-allocated list and the upgrade point living in the Diagram rather than being restated beneath it.

260726 · The alignment ran, on JL's go, in the four phases the Diagram had set out. Twelve skills, plus the shared anatomy spec and 90 venue templates. Two rulings were settled on the way rather than deferred. The Gate Ledger landed in each S page's `## Log`, which unblocked retiring `STATUS.md` entirely; that in turn retired `DRIFT`, which had only ever named the gap between a stored frontier and the disk. And the venue pin moved into `S-Venue-0-venue.md` frontmatter, so one page owns the venue contract. The `0-seed` contract's four-line loopback warning was deleted rather than reworded: it existed to stop a re-run demoting a stored `current_layer`, and with nothing stored there is nothing to demote.

260726 · JL asked the Diagram to say which skills this rule changes and whether they are done. `WHO WRITES WHAT` gained an UPDATED column with per-skill counts, split into old-path debt and `STATUS.md` debt, and a second block saying what each of the four rewrites actually was. The measurement moved the priority: `haipipe-paper-stage` (22 old-path, 12 `STATUS.md`, across eight run-time stage contracts) is worse than `enter`, which the earlier `SKILL.md`-only count had put first.

260726 · The four `1-build/` skills rewritten against this face, on JL's go. `conform` 0.2.0 is the one that matters: the delete test stopped being a convention and became block J of `check_structure.sh`, which resolves every target a master reaches and asserts none sits behind a number. It fails the MISQ paper with 56 findings. `folder` 0.5.0, `scaffold` 0.2.0 (six templates rewritten, not just prose) and `restructure` 0.2.0 followed. `conform` first was deliberate: it is read-only, so it could not break anything, and once correct it is the pass/fail check the other three are written against.

260726 · JL asked what separates `displays/` from `figures/`. Nothing does, and that was an error in this diagram carried over from the pre-unit npjDM2025 layout: `figures/` on the MISQ paper holds 5 orphan PNGs no `\includegraphics` points at. `figures/` deleted from the layout, and the unit expanded to show its real 8 members and which 2 ship. Same turn, JL proposed retiring `STATUS.md` and the stage strip; the argument and the one blocker are in Discussion.

260726 · JL asked which skills this face is about, so the Diagram gained a WHO WRITES WHAT block: one author per line of the tree. Writing it exposed the real gap. The ruling was assumed to be one stale skill (`haipipe-paper-folder`); measuring found 15 `SKILL.md` carrying 63 old-layout mentions, all four `1-build/` skills among them, and the MISQ paper's own top level still failing the delete test. Items and Where we are rewritten against those counts.

260727 · Corrected a ruling reported as a fact. This face said eight families and eight folders; the board tooling knows seven. `Round` was ruled a family on 260726 and `FAMILIES` in `haipipe-board/stage.py:25` was never updated, so `resolve_filename("Round", …)` raises and the live `7-round/` holds only `_archive/`. Found while a subagent re-verified `QB2b`'s addressing claims against the code rather than against this page.
