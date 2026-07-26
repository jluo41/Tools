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
  What is on the board inside it is `QA7`; how a question leaves it is `QA5`; markdown versus tex authority is `QB6`; who creates a page is `QA8`; what a display unit contains is `QC3` and `QD1`.

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
        board.md/html   /haipipe-board            ③   ➖  owns its rule
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
Inside `0-lifecycle/`, the folder name IS the S family name: eight families, eight folders. Before 260726 the folders carried the old STAGE order and the two disagreed badly. `Work` was split across `1a-resource/` and `1b-claims/`, `Venue` across three, and `5-section-edit/` held Main, Appendix and Submission at once while Submission was also split with `6-submission/`. Nine folders, eight families, and not one clean mapping.

A reader can now place a page from its name alone: `S-Main-7-results.md` is in `4-main/`, and nothing else could be.

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
- [x] 🌱 Choose a minimal scaffold
      A new paper receives no speculative LaTeX, no section stubs, and no page for a unit nobody has asked for.
- [x] 🧭 Make the scaffold Board-first
      `0-lifecycle/board.md` and one Seed page make a new paper runnable immediately.
- [x] 🔢 Number by deletability
      `0-` `1-` `2-` is working machinery, unnumbered is the deliverable, and `rm -rf 0-* 1-* 2-*` is the test (JL 260726).
- [x] 🗂 One family, one folder
      Eight S families, eight folders inside `0-lifecycle/`; 40 pages migrated on the MISQ paper with none lost.
- [x] 🖼 Delete `figures/` from the layout
      It predates display units. On the MISQ paper it holds 5 orphan PNGs that no `\includegraphics` in the paper points at, while every real graphic already sits in a unit's `assets/`. A second home for the same thing is the defect this face forbids elsewhere.
- [ ] ✂️ Rule where a display unit's working half lives
      2 of a unit's 8 members ship: `float.tex` and `assets/`. `README.md`, `preview.tex`, `preview.pdf`, `source/`, `candidates/` and `versions/` never do, so `displays/` fails the delete test as it stands. See Discussion.
- [x] 🛠 Teach the four BUILD skills this layout
      Done 260726. `conform` 0.2.0 rewritten around the delete test as an executable check (block J) plus board purity (block D), and it now fails the MISQ paper with 56 findings. `folder` 0.5.0 scaffolds Board-first with one runnable Seed page and creates no `STATUS.md`. `scaffold` 0.2.0 reframed as the manuscript upgrade, with its six templates rewritten, not just its prose. `restructure` 0.2.0 migrates INTO the new shape and gained the delete test as a third non-negotiable gate.
- [x] 🧹 Align the remaining skills with this layout
      Done 260726, in four phases ordered by BINDING rather than by mention count. ① `haipipe-paper-stage` 0.7.0: eight `stages/*/stage.md` contracts, whose `artifact:`/`probes:`/`units:`/`output:` resolve at run time, so a stale one does not read wrong, it WRITES to the wrong place. ② `haipipe-paper-enter` 0.5.0, the console. ③ `haipipe-paper-lifecycle` 0.4.0, the router. ④ the tail: `probe` 0.7.0, `draft-display` 0.2.0, `diffpdf` 0.2.0, `compile` 0.2.0, `revise` 0.2.0.
      Two things the plan had not counted, both found by measuring directories instead of `SKILL.md`: `2-phase/REF/paper-folder-anatomy.md`, the shared spec every build skill cites, whose prefix table asserted the OPPOSITE rule and is the reason the family drifted; and 90 venue templates carrying one identical stale line.
- [x] 📍 Rule STATUS.md out of existence
      Adopted 260726 on JL's proposal, with the Gate Ledger landing in each S page's `## Log`, one row on the page whose gate it was. That was the only blocker: it is the one part of the file that is history and cannot be re-derived. `current_layer`/`maturity` are derived from disk; the `venue:` pin moved to `S-Venue-0-venue.md` frontmatter. `folder` no longer creates the file, `conform` warns when one exists, `restructure` migrates its rows out before removing it, and `DRIFT` was retired with it: it named the gap between a stored frontier and disk, and there is no stored frontier. What replaced it is narrower and real, `STALE`, an S page whose own `state:` over-claims about itself.
- [ ] 🧨 Make the MISQ paper pass its own test
      Only `0-lifecycle/` was migrated. The top level still holds `0-sections/`, `0-<paper>.tex/.bib/.pdf`, `1-compile.sh`, `1-rounds/`, an empty `1-board/` and an `0-extra/` junk drawer, so `rm -rf 0-* 1-*` deletes the manuscript.
- [ ] 🧪 Create one paper and enter it
      A fresh agent should open its Board and work Seed without adding or guessing another control file.

## Where we are
The layout is ruled, and exactly one folder has been built to it: `0-lifecycle/` on the MISQ paper, eight family folders holding 40 S pages relocated with every name preserved, and all Links and stage contracts repointed and verified.

The rule now also lives somewhere a machine can read it. The four `1-build/` skills were rewritten on 260726, and `haipipe-paper-conform` 0.2.0 turned the delete test from a convention into a check: block J resolves every `\input`, `\includegraphics` and `\bibliography` target a master reaches and asserts none sits behind a number. Run against the MISQ paper it exits 1 with 56 findings, 18 of them delete-test failures including the driver `.tex` and the `.bib`. Before, nothing could tell you whether a paper folder was correct, and `conform` would have failed a folder that was.

The rest of the family has now been told too. Twelve skills were aligned on 260726, ordered by binding rather than by mention count: the eight stage contracts first, then the console, the router, and the tail. With them went the two things a `SKILL.md`-only count had missed: `2-phase/REF/paper-folder-anatomy.md`, the shared spec every build skill cites, whose prefix table asserted the opposite rule and is the reason the family drifted at all; and 90 venue templates carrying one identical stale line.

What is left is the papers, not the skills. The MISQ paper is still unmigrated above `0-lifecycle/`, which is exactly what those 56 findings are, and `restructure` 0.2.0 now knows how to fix it.

Two things remain open, and this page stays 🟡 until they close. `STATUS.md` is proposed for deletion rather than merely undecided (JL 260726), and what blocks it is one question: where the Gate Ledger goes, since it is the only part of that file that is history and not derivable. And the purity rule is aspirational in one place: `3-display/` still holds `4-display.tex`, `4-display.pdf` and a `_DISPLAY_REQUEST.md` sidecar, which are build products and a forbidden file sitting inside the board, blocked on `QB2`'s grain ruling.

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
260726 · Rounds moved inside the lifecycle as an eighth family, one page per round. Folders renumbered to one-family-one-folder; 40 pages migrated with none lost. Numbered-versus-unnumbered adopted as the delete test on JL's ask. Page then rewritten clean: three Content divisions instead of seven, with the scaffold, the absent-until-allocated list and the upgrade point living in the Diagram rather than being restated beneath it.

260726 · The alignment ran, on JL's go, in the four phases the Diagram had set out. Twelve skills, plus the shared anatomy spec and 90 venue templates. Two rulings were settled on the way rather than deferred. The Gate Ledger landed in each S page's `## Log`, which unblocked retiring `STATUS.md` entirely; that in turn retired `DRIFT`, which had only ever named the gap between a stored frontier and the disk. And the venue pin moved into `S-Venue-0-venue.md` frontmatter, so one page owns the venue contract. The `0-seed` contract's four-line loopback warning was deleted rather than reworded: it existed to stop a re-run demoting a stored `current_layer`, and with nothing stored there is nothing to demote.

260726 · JL asked the Diagram to say which skills this rule changes and whether they are done. `WHO WRITES WHAT` gained an UPDATED column with per-skill counts, split into old-path debt and `STATUS.md` debt, and a second block saying what each of the four rewrites actually was. The measurement moved the priority: `haipipe-paper-stage` (22 old-path, 12 `STATUS.md`, across eight run-time stage contracts) is worse than `enter`, which the earlier `SKILL.md`-only count had put first.

260726 · The four `1-build/` skills rewritten against this face, on JL's go. `conform` 0.2.0 is the one that matters: the delete test stopped being a convention and became block J of `check_structure.sh`, which resolves every target a master reaches and asserts none sits behind a number. It fails the MISQ paper with 56 findings. `folder` 0.5.0, `scaffold` 0.2.0 (six templates rewritten, not just prose) and `restructure` 0.2.0 followed. `conform` first was deliberate: it is read-only, so it could not break anything, and once correct it is the pass/fail check the other three are written against.

260726 · JL asked what separates `displays/` from `figures/`. Nothing does, and that was an error in this diagram carried over from the pre-unit npjDM2025 layout: `figures/` on the MISQ paper holds 5 orphan PNGs no `\includegraphics` points at. `figures/` deleted from the layout, and the unit expanded to show its real 8 members and which 2 ship. Same turn, JL proposed retiring `STATUS.md` and the stage strip; the argument and the one blocker are in Discussion.

260726 · JL asked which skills this face is about, so the Diagram gained a WHO WRITES WHAT block: one author per line of the tree. Writing it exposed the real gap. The ruling was assumed to be one stale skill (`haipipe-paper-folder`); measuring found 15 `SKILL.md` carrying 63 old-layout mentions, all four `1-build/` skills among them, and the MISQ paper's own top level still failing the delete test. Items and Where we are rewritten against those counts.
