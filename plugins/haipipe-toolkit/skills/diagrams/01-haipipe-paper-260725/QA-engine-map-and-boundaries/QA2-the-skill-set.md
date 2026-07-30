# ① The skill set: what ships
state: 🟡 PARTIAL
owner: JL
method: one responsibility per layer, one direction of control, progressive disclosure inside each skill

## Question
What is in the reusable skill package, what runs at each stage, and what does it put into the other folders? This is the one folder written once and used by every paper: 35 skills and 7,406 lines, each of them a promise that some stage worker will follow. The work here is ownership, not layout.

This is one of three folders written once and used by every paper, `③` being the other. Everything in it is a promise: a contract a stage worker will follow, a script that will run, a template that will be filled. Nothing in it is about any particular paper, and the moment something here mentions one, it has stopped being reusable.

The folder is already close to the right architecture, so the useful work is not a directory migration. It is ownership. Several skills still carry routing, craft, rendering, history and state at once, and the front door has grown to 556 lines, which every invocation pays for whether or not it needs them.

What is genuinely missing is the second half of the question above. A reader can see which layers exist and cannot see what a stage RUN actually does: which workers it dispatches, what it writes, where it writes it, and what appears in the paper as a result. That is the part this face now carries, because it is also the map of how `①` touches `⑦` and `⑧`.

## Boundary
- ✅ Covered here
  The layers, the direction of control, the anatomy of one callable skill, what each of the eight stages runs and produces, and what crosses this folder's edges.
- ↪ Covered elsewhere
  Which folder this is among the four is `QA1`; the design board that rules it is `QA3`; the paper it writes into is `QA6` and that paper's board is `QA7`; the contract form itself is `QE1`; the Display split is `QD1`.

## Diagram
```
   one request, one direction, no second orchestrator
   ② WHICH BOARD GROUP RULES IT · the layer · what it LEAVES BEHIND

   ruled by ②        user intent
                         │
                         ▼
   QA2 ──────────▶  haipipe-paper/   THE SINGLE DOOR. the only thing a human
   QA1                   │           types. resolve the paper, CALL ③ to build
   QA4                   │           and open ⑧, route. WHICH, never HOW.
                         │           writes NOTHING · renders NOTHING
                         │           → calls ③ haipipe-board   (the human channel)
                         │           → calls ⑤ haipipe-probe   (the evidence channel)
                         ▼
   QA6 ──────────▶  0-enter/         which paper, which round
   QA7                   │           → ⑦  .paper-console.yaml   session state
                         │           → ⑧  S-Round-<n>-<vYYMMDD>.md
                         │                and that round's letters beside it
                         ▼
   QB1-QB3d ──────▶  1-lifecycle/     pick ONE S page, load ONE stage contract
   QA8  (creation)       │           haipipe-paper-stage · index.yml · 8 contracts
   QE   (the form)       │           → ⑧  S-<Family>-<unit>-<slug>.md
                         │                create-page.py calls the Board's stage.py
                         ▼
   QB3-QB3d (phases) ─▶ 2-phase/   the four phases, 13 workers, all on ONE page
   QC   (sentence)       │
   QA9  (the runner)     │  DRAFT   → ⑧  the page's ## Content + its Q-consumer
                         │  PROBE   → ⑦  1-probes/PPnn_<topic>/QXn_<slug>.md
                         │           ↳ ACROSS THE WALL, read-only, to
                         │             tasks/ · discoveries/ → QA/<n>-<slug>.md
                         │             The answer is never copied in; it is pointed at.
                         │  REVISE  → ⑧  the same page, plus %% why-comments
                         │  CHECK   → ⑧  state: ✅   WRITTEN BY A HUMAN
                         ▼
```

```
   …continuing DOWN the same chain, the artifact side ──────────

   QB2d (the product) ──▶ 3-deliver/  1-build · 2-audit · 3-polish · 4-ship
   QD   (renderers)      │           → ⑦  sections/*.tex   GENERATED from ⑧
                         │           → ⑦  displays/…/float.tex
                         │           → ⑦  main.pdf · overleaf · the bundle
                         ▼
   QA7 ──────────▶  4-respond/       → ⑧  the round's S-Round page: what came
                         │                back, what was decided, what applied
                         ▼
   QD  ──────────▶  5-present/       → ⑦  slides.pdf · poster.pdf, from the
                                          ACCEPTED paper

```

```
   ── read the LEFT column and the graduation edge is addressable ──
      every layer here is ruled by some group on ②. A Law that reaches ✅
      has a named target, so "it is decided" and "it is applied" stop
      being the same sentence. QA3 is the only group with no target at
      all, because it rules the board itself.

   ── read the RIGHT column and the placement rule falls out ───────
      ⑧ gets everything a stage DECIDES or writes as prose
      ⑦ gets everything GENERATED from those decisions, plus the
        evidence pointers
      ① gets NOTHING. Nothing a paper run produces is written back into
        the skill: that direction is graduation, and only ② may travel it.

   ── which layers are ADAPTERS, and onto what ─────────────────────
      1-lifecycle/  create-page.py ──▶ ③  the Board's stage.py
      2-phase/      haipipe-paper-probe ──▶ ⑤  "only the paper-side deltas"
      every other layer writes ⑦ or ⑧ directly and adapts onto nothing.

   consulted, never in the chain of command:
     venue/     knowledge packs, read lazily. NEVER lifecycle verbs.
     diagram/   design Boards.               NEVER runtime contracts.

   ───────────────── zoom in on any one skill ─────────────────

   tier 1  metadata        name + description     selects the skill, always paid
   tier 2  SKILL.md        the core loop          paid on every invocation
   tier 3  references/     loaded ONLY when its branch is taken
           scripts/        run without consuming reasoning context
           assets/         copied into outputs

   ✗ never in the invocation path, at any tier:
     CHANGELOG.md · feedback/ · migration notes · status reports · design Boards
```

## Content
### The family layers
```
haipipe-paper/   thin front door: resolve paper, open Board, route intent
0-enter/         create or enter a paper and manage dated rounds
1-lifecycle/     stage contracts and the Board-aware stage runner
2-phase/         internal DRAFT, PROBE, REVISE, and CHECK workers
3-deliver/       build, render, audit, compile, export, and ship
4-respond/       rebuttal and revision response
5-present/       slides and posters derived from the accepted paper
venue/           lazily consulted knowledge packs, never lifecycle verbs
diagram/         design Boards, never runtime contracts
```
The front door selects context. The stage runner works one S page and dispatches a bounded worker. Workers return results to the same page. Delivery adapters materialize accepted Content into target formats. There is no second orchestrator anywhere in that chain.

### What every stage runs
The same four phases, dispatched to the same thirteen workers, whichever stage is running.
```
DRAFT    haipipe-paper-draft          raises questions, writes nothing it cannot source
         ├── draft-citation           finds assertions owing a source. READ-ONLY.
         ├── draft-values             finds numbers owing a run
         └── draft-display            finds claims owing a display
PROBE    haipipe-paper-probe          the ONLY door evidence enters by; crosses the
                                      wall to tasks/ and discoveries/
REVISE   haipipe-paper-revise         rewrites to venue quality, leaves why-comments
         ├── revise-place             substitutes LANDED answers into placeholders
         ├── revise-content           section → paragraph → weave → sentence
         ├── revise-humanizer         removes AI tells
         └── revise-results           results prose
CHECK    haipipe-paper-check          HUMAN GATE. Only a person may pass it.
         ├── check-evidence
         └── proof-checker
```

### What each stage writes, and what appears in the paper
```
 stage          phases        writes into ⑧ the paper board      generates in ⑦
 ────────────   ───────────   ─────────────────────────────────  ──────────────────
 seed           D P R C       S-Seed-0-seed.md                   —
 resource       D P R C       S-Work-0-resources.md              —
 claims         D P R C       S-Work-1-claims.md                 —
 venue          D P   C       S-Venue-0-venue.md                 STATUS.md `venue:`
                no REVISE     (a contract, not prose, so there
                              is nothing to polish)
 pitch          D P R C       S-Venue-1-pitch.md                 —
 narrative      D P R C       S-Venue-2-narrative.md             —
 display        D P R C       per-unit, blocked on QB2b           4-display.tex
                              (11 S-Display pages on MISQ)       displays/…/
 section-edit   D P R C       S-Main-n · S-Appendix-x            sections/*.tex
                PER UNIT      one page per section
```
Five of the eight produce nothing in `⑦` at all: their whole product is a page in `⑧`. Only display and section-edit generate manuscript files, and both generate them FROM the page, never the other way round.

### The anatomy of one skill
```
<skill-name>/
├── SKILL.md       trigger and shortest complete execution procedure
├── references/    detailed contracts and variants, loaded only when needed
├── scripts/       deterministic operations that should not be rewritten
├── assets/        templates or files copied into outputs
└── agents/        optional discovery and UI metadata
```
Metadata selects the skill. `SKILL.md` explains the core loop and names exactly which conditional reference to read. Scripts and assets do work without consuming routine reasoning context.

Design Boards, changelogs, feedback archives, migration narratives and status reports do not belong in the live invocation path. If history must be retained, keep it outside the callable skill folder. The evidence that this is not theoretical: `haipipe-paper/SKILL.md` is 556 lines and owns routing, closing UI, comment history, evidence routing and delivery needs at once; `haipipe-display-poster/SKILL.md` is 854.

### The roster: 35 skills, with versions
Measured 2026-07-26. `ver` is the skill's own `metadata.version`; `lines` is its `SKILL.md`, which is what every invocation of it pays for.
```
 layer            skill                             ver     updated     lines
 ──────────────   ───────────────────────────────   ─────   ──────────  ─────
 front door       haipipe-paper                     0.3.2   2026-07-19    556  ⚠
 0-enter          haipipe-paper-enter               0.4.1   2026-07-19    570  ⚠
                  haipipe-paper-round               0.1.0   2026-07-19    168  ⚠ superseded
 1-lifecycle      haipipe-paper-lifecycle           0.3.1   2026-07-19    422
                  haipipe-paper-stage               0.6.0   2026-07-25    235
 2-phase/draft    haipipe-paper-draft               0.5.2   2026-07-19    416
                  haipipe-paper-draft-citation      0.1.1   2026-07-19    122
                  haipipe-paper-draft-display       0.1.1   2026-07-19    116
                  haipipe-paper-draft-values        0.1.1   2026-07-19    116
 2-phase/probe    haipipe-paper-probe               0.6.1   2026-07-19    219
 2-phase/revise   haipipe-paper-revise              0.1.6   2026-07-19    158
                  haipipe-paper-revise-content      0.1.4   2026-07-19     84
                  haipipe-paper-revise-humanizer    0.2.3   2026-07-07    130
                  haipipe-paper-revise-place        0.1.0   2026-07-19    111
                  haipipe-paper-revise-results      0.2.3   2026-07-08     86
 2-phase/check    haipipe-paper-check               0.3.0   2026-07-19    442
                  haipipe-paper-check-evidence      0.1.0   2026-07-19    148
                  haipipe-paper-proof-checker       0.1.2   2026-07-19    369
 3-deliver/build  haipipe-paper-conform             0.1.1   2026-07-19     81
                  haipipe-paper-folder              0.4.0   2026-07-14    131
                  haipipe-paper-restructure         0.1.1   2026-06-04    110
                  haipipe-paper-scaffold            0.1.1   2026-06-04    120
 3-deliver/audit  haipipe-paper-claim-audit         0.1.1   2026-05-31    230
                  haipipe-paper-optimizer           0.1.1   2026-05-31    346
                  haipipe-paper-reviewer            0.1.1   2026-05-31    148
 3-deliver/polish haipipe-paper-polish              0.1.0   2026-07-17     56
 3-deliver/ship   haipipe-paper-compile             0.1.0   2026-05-31    287
                  haipipe-paper-diffpdf             0.1.1   2026-07-19    350
                  haipipe-paper-to-overleaf         0.1.1   2026-07-19    239
 3-deliver        haipipe-paper-deliver             0.1.0   2026-07-19    163
 4-respond        haipipe-paper-rebuttal            0.1.1   2026-07-14    310  ⚠
                  paper-rebuttal                    0.1.1   2026-07-14    146  ⚠
                  rebuttal-response                 0.1.0   2026-05-31    171  ⚠
 5-present        paper-poster                      0.2.0   2026-07-24    134
                  paper-slides                      0.2.0   2026-07-24    136
 ──────────────   ───────────────────────────────   ─────   ──────────  ─────
                  35 skills                                            7,406
```

Four things this roster says that no prose on this page did.

**Nothing has reached 1.0.** Every skill is `0.x`, and eleven are still `0.1.x`. That is honest rather than alarming, but it means no part of this folder has ever been declared stable, and `QE2`'s fresh-agent acceptance has never been passed by any of them.

**The compaction problem is bigger than the front door.** `haipipe-paper` is 556 lines and `haipipe-paper-enter` is 570, so the two files a session reads first total 1,126 lines before any actual work is selected. `haipipe-paper-check` adds 442 and `haipipe-paper-draft` 416. `QA3`'s progressive-disclosure Law is stated and, by these numbers, not applied anywhere.

**`4-respond/` has three overlapping rebuttal skills**: `haipipe-paper-rebuttal` (310), `paper-rebuttal` (146) and `rebuttal-response` (171). Nothing on this board rules which is the entry, and two of them predate the third. That is the clearest single ownership defect in the folder.

**The naming is not uniform.** Four skills drop the `haipipe-` prefix: `paper-rebuttal`, `rebuttal-response`, `paper-poster`, `paper-slides`. A reader cannot tell from a name whether a skill belongs to this family, which matters because the prefix is how the family is discovered.

### Which board group rules which skill
This is the `② ──graduates──▶ ①` edge, made addressable. Every group on the design board rules some part of this folder, and a ruling that reaches ✅ has to land somewhere concrete or it has not graduated. This is that target list, so nobody has to guess.
```
 board group                   what it rules in ①                        state
 ───────────────────────────   ───────────────────────────────────────   ─────
 QA1  six folders              README.md · PHILOSOPHY.md                  ✅
       the family map that should carry the boundary and does not yet
 QA2  the skill set            the tree layout · haipipe-paper/SKILL.md   🟡
       THIS page. 556 lines at the front door is its open item.
 QA3  the skill board          NOTHING in ①, by design                    🟡
       it rules the board itself; that is what makes ② deletable
 QA6  the paper                haipipe-paper-folder/SKILL.md              🟡
                               haipipe-paper-enter/SKILL.md
       the scaffold contract. Already changed once today: 3 containers.
 QA7  the paper board          haipipe-paper-round/SKILL.md   <- REWRITE  🟡
                               haipipe-board's S-family list
       the round ruling landed here and the skill still contradicts it
 ───────────────────────────   ───────────────────────────────────────   ─────
 QB1-QB2b  adding a stage       stages/index.yml . CONTRACT.md . SKILL.md  🟡
       the test that admits one, the four files, the two variation flags
 QB2a  the stage template      stages/*/template.md  x8                   🔴
       create-page.py PARSES it; the file says "follow, don't ship"
 QB2b-QB2d  the page it writes   create-page.py . haipipe-board/stage.py    🟡
       who names it, what a second run does, what is generated from it
 QB3-QB3d the four phases      2-phase/  x4 . ref/08-stage-gate.md        🟡
       calling them, then DRAFT, PROBE, REVISE and the gate
 QA8  who owns the page        create-page.py . haipipe-board/stage.py    🟡
       the one-file rule, dependencies, state, creation
 QA9  how work is DRIVEN       haipipe-paper-stage/SKILL.md (the runner)  🟡
                               haipipe-board/serve.py (the live layer)
 ───────────────────────────   ───────────────────────────────────────   ─────
 QC   the sentence             2-phase/0-draft/draft-{citation,values,    🟡
                                 display}/ . 2-phase/2-revise/revise-place/
                               stages/5-section-edit/template.md
                               haipipe-board/src/body.py (the chips)
 QD   the display              display/ (the reusable family)             🟡
                               1-lifecycle/4-display/ref/
                               3-deliver/ renderers
 QE   shipping                 stages/index.yml . stages/CONTRACT.md      🟡
```

Three things fall out of reading it as a column.

`QA3` is the only group with no target in `①`, and that is not an omission. It rules the design board itself, which is exactly why `②` can be deleted without breaking anything.

`QA4`, `QA8`, `QA9`, `QC` and `QD` each name a file in `board/haipipe-board/` or `display/`, which are not inside this folder at all. Those are the rulings that cross a package boundary, and they are the ones most likely to be half-applied: a Law can graduate into the paper skill and quietly not reach the board tool that implements its other half.

`QA7` is the live example of a ruling that landed and has not been carried: the round ruling is written on the board and `haipipe-paper-round/SKILL.md` still describes the layer it removed. It carries a superseded banner rather than a rewrite, so the gap is visible instead of silent.

### What crosses this folder's edge
```
 ② the skill board  ──▶ ①    IN, and only this way. A ruling reaches ✅ and its
                             Law is COPIED into a SKILL.md, a stage contract, or
                             a ref/ file. Nothing here may read the board back.

 ① ──▶ ⑦ the paper           OUT, only through a stage run. A worker writes the
                             page and any generated manuscript file. No skill
                             file is ever copied into a paper.

 ① ──▶ ⑧ the paper board     OUT, and this is the one people forget. Creating a
                             page is `create-page.py`, which selects the stage
                             and template here, then calls haipipe-board's
                             `stage.py` for the shell. Board owns the filename,
                             Paper owns the Content jobs.

 ① ──▶ the wall              NEVER directly. Only the PROBE worker crosses to
                             tasks/ and discoveries/, and it asks; it does not run.
```

### What changes here, and how often
```
 rarely    the layer map, the anatomy, the phase list           a QA/QB ruling
 per rule  a stage contract's fields                            a graduated Law
 per venue a pack under venue/                                  a new outlet
 never     anything naming one paper                            that is ⑦ or ⑧
```

## Items to Finish
- [x] 🗂 Keep the numbered family spine
      The existing top-level organization remains useful and avoids a migration with no user benefit.
- [x] ✂️ Choose progressive disclosure
      One short SKILL.md points directly to conditional references, scripts, and assets.
- [x] 🔭 Say what a stage RUN does, not just which layers exist
      The four phases, the thirteen workers, and the per-stage write and generate table (260726, JL's ask).
- [x] 🔀 State this folder's three edges
      What comes in from `②`, what goes out to `⑦` and `⑧`, and that only PROBE crosses the wall.
- [x] 🎯 Map every board group to what it rules here
      The graduation edge is addressable: each group names the files a settled Law must land in (JL 260726).
- [ ] 🔗 Carry the cross-package rulings
      QA4, QA8, QA9, QC and QD each rule a file in `haipipe-board/` or `display/`, outside this folder. Nothing checks that a Law reached both halves.
- [x] 📋 List the roster with versions
      35 skills, their versions, dates and SKILL.md sizes, measured 260726.
- [ ] 🧠 Rule which rebuttal skill is the entry
      `4-respond/` carries three: `haipipe-paper-rebuttal`, `paper-rebuttal`, `rebuttal-response`. Nothing says which one a session calls, and two predate the third.
- [ ] 🏷 Make the naming uniform
      Four skills drop the `haipipe-` prefix, which is how the family is discovered.
- [ ] ✂️ Make the front door thin
      Move stage craft, comment detail, evidence detail, and output-specific rules to their actual owners. 556 lines paid on every invocation.
- [ ] 📏 Set a compactness acceptance test
      A fresh agent should identify the entry, stop conditions, and next owner without reading family history.
- [ ] 🧹 Inventory the current paper skills
      Classify every extra file as runtime reference, deterministic script, reusable asset, or design history.
- [ ] 🧠 Rule what a stage may write into `⑦` directly
      Today only display and section-edit generate manuscript files, and only from their page. Whether any stage may write to `⑦` without a page is unstated, and a worker with a plausible reason will eventually do it.
- [ ] 🧪 Trace one request through the layers
      A fresh session should move from Board to stage runner to worker to the same page without another orchestrator.

## Where we are
The ownership map, the anatomy, and the per-stage run map are recorded, and on 260726 a large slice of it was finally APPLIED rather than only argued. Sixteen of the 35 skills were rewritten against `QA6`'s layout ruling in one pass, ordered by which held a live binding rather than by how many stale mentions each had: the four `1-build/` skills first (with `conform` first of those, because it is read-only and once correct it becomes the pass/fail test the other three are written against), then the eight stage contracts, the console, the router and the phase tail. The shared spec `2-phase/REF/paper-folder-anatomy.md` went with them, and it mattered most: its prefix table asserted the exact inverse of the delete test, which is why the family had drifted at all.

The front door was applied too. `haipipe-paper` is now the single thing a human types, and it calls `③` and `⑤` rather than sitting beside them (`QA4`).

What is still only argued is the ownership cleanup this face opened with: several skills continue to carry routing, craft, rendering, history and state at once.

The two zoom levels, family and folder, were separate faces until 260726, when they merged: both answer "what is inside `①`", and splitting them put two of QA's four faces on one quadrant.

Reopened to 🟡 on 260726: the edge map raised a real unruled question, which is whether a stage may write into `⑦` without going through a page.

## Files
- `haipipe-paper/SKILL.md`
  The front door, and the largest compaction candidate at 556 lines.
- `1-lifecycle/haipipe-paper-stage/`
  The runner, `stages/index.yml`, the eight contracts, and `CONTRACT.md`.
- `2-phase/`
  The thirteen phase workers.
- `3-deliver/`
  The output and shipping family.

## Law
The numbered family spine stays. Each layer owns one responsibility and control flows one way: the front door selects context, the stage runner works one S page, a bounded worker returns to that same page, delivery adapters materialize accepted Content.

`venue/` is knowledge consulted lazily and never carries a lifecycle verb. `diagram/` holds design Boards and never a runtime contract. Neither is in the chain of command.

Inside one skill: progressive disclosure. Metadata selects, `SKILL.md` carries the shortest complete procedure and names which conditional reference to read, and everything else loads only when its branch is taken. Design history never sits in the invocation path.

Nothing in this folder names one paper. A rule that mentions a specific manuscript belongs in `⑦` or `⑧`, not here.

## Log
260726 · The map stopped being only a map. 16 skills aligned to `QA6`'s layout in one pass, plus the shared anatomy spec and 90 venue templates; the front door became the single door (`QA4`). The diagram's front-door box now names both dispatches. One correction the pass produced belongs here: measuring per SKILL.md badly understated the work, because `haipipe-paper-stage`'s real debt was in its eight `stages/*/stage.md` contracts, whose paths RESOLVE AT RUN TIME. A stale path in a contract does not read wrong; it writes to the wrong place.

260726 · Added what a stage RUN does (13 workers, the per-stage write/generate table), the roster of 35 skills with versions, and the map of which board group rules which skill. The diagram gained a left column naming the ruling group per layer, on JL's ask. Reopened to 🟡: the edge map raised an unruled question, whether a stage may write into `⑦` without going through a page.
