# ① The skill set: what ships
state: 🟡 PARTIAL
owner: JL
method: one responsibility per layer, one direction of control, progressive disclosure inside each skill
session: 582e6b19-40ad-4fe2-91b3-253835dc92d2

## Opening
What is in the reusable skill package, what runs at each stage, and what does it put into the other folders?
This is the one folder written once and used by every paper: ONE registered skill and nine stage contracts in ten stage data folders, each of them a promise a stage run will follow. The work here is ownership, not layout.

This is one of three folders written once and used by every paper, `③` being the other. Everything in it is a promise: a contract a stage worker will follow, a script that will run, a template that will be filled. Nothing in it is about any particular paper, and the moment something here mentions one, it has stopped being reusable.

The folder has now had its directory migration four times over (260803 SNN move, thin-paper phases 1, 2 and 3), and the ownership work landed with it. The end state is one registered skill: a 699-line door that replaced four routers, a container pair, five build tools and two round skills; an invocation pays the door, the small stage index, and exactly ONE stage.md, and the phase machinery the family used to carry is rented from `board/`.

What is genuinely missing is the second half of the question above. A reader can see which layers exist and cannot see what a stage RUN actually does: which phases it runs, what it writes, where it writes it, and what appears in the paper as a result. That is the part this face now carries, because it is also the map of how `①` touches `⑦` and `⑧`.

Scope: This page covers The layers, the direction of control, the anatomy of one callable skill, what each of the nine stages runs and produces, and what crosses this folder's edges. Neighbouring pages cover Which folder this is among the eleven is `QA1`; the design board that rules it is `QA3`; the paper it writes into is `QA6` and that paper's board is `QA7`; the contract form itself is `QF2`; the Display split is `QBe2 §3`.

## Diagram
```text
   one request, one direction, no second orchestrator
   ② WHICH BOARD GROUP RULES IT · the step · what it LEAVES BEHIND

   ruled by ②        user intent
                         │
                         ▼
   QA2 ──────────▶  haipipe-paper/     THE ONE DOOR (0.7.0), and since phase 3 the
   QA1  QA4              │             family's ONLY registered skill. the only
   QA6 (get-or-create)   │             thing a human types. enter/status open ⑧
                         │             through ③; it renders NOTHING and
                         │             computes NOTHING itself.
                         │             → calls ③ haipipe-board   (the human channel)
                         │             → calls ⑤ haipipe-probe   (the evidence channel)
                         │             owns --depth spend authority · probe/ tooling
                         │             · ref/enter-console.md · fn/
                         ▼
   QC2  QF2 ─────▶  stages/index.yml   the small index, read on every invocation
                         │             verb → ONE stage key → load ONE stage.md,
                         │             NEVER the other eight
                         ▼
   QC3-QC3d  QA8 ─▶ create-page.py     ensure the S page: select the stage
                         │             template here, call ③'s cli/stage.py for
                         │             the filename and shell
                         │             → ⑧  S-<Family>-<unit>-<slug>.md
                         ▼
   QC4-QC4d  QA9 ─▶ haipipe-page WORK ON / RUN. the page work is ③'s;
   (rented from ③)       │             each phase loads, in order: base page →
                         │             for-stage variant → phase contract → the
                         │             stage's craft: files
                         │  DRAFT   → ⑧  the page's ## Content + its Q-consumer
                         │  PROBE   → ⑧  an S03/S04 evidence page's E<n>
                         │             division + its hidden QA-probe under
                         │             probes/L|V<nn>-<topic>/<n>-<slug>.md
                         │           ↳ ACROSS THE WALL, read-only, to
                         │             tasks/ · discoveries/ → QA/<n>-<slug>.md
                         │             The answer is never copied in; it is pointed at.
                         │  REVISE  → ⑧  the same page, plus %% why-comments
                         │  CHECK   →    runs the declared checker: script, then
                         │              the HUMAN GATE → ⑧  state: ✅
                         ▼
                    rebuild the board  ③'s build.py, after every write
```

```text
   …continuing DOWN the same chain, the artifact side ──────────

   QB5  QB6 ───────▶ display · section-edit   the only two stages that generate
                         │                    manuscript files, always FROM the page
                         │            → ⑦  displays/<unit>/ via the four
                         │                 commissioned renderers
                         │            → ⑦  sections/*.tex, generated by sync
                         ▼
   QB9 ──────────▶  the door's        compile · diffpdf · project · to-overleaf
                         │  build verbs  · to-word, each an fn/ procedure over
                         │               scripts/, with S09-build/proof-checker/
                         │               as the craft pack
                         │            → ⑦  main.pdf · diff.pdf · overleaf ·
                         │                 word bundle · projection
                         ▼
   QB10  QA7 ────▶  S10-round/round/  the round STAGE, with rebuttal-craft.md
                                      → ⑧  the round's S page: what came back,
                                           what was decided, what applied
```

```text
   ── read the LEFT column and the graduation edge is addressable ──
      every step here is ruled by some group on ②. A Law that reaches ✅
      has a named target, so "it is decided" and "it is applied" stop
      being the same sentence. QA3 is the only group with no target at
      all, because it rules the board itself.

   ── read the RIGHT column and the placement rule falls out ───────
      ⑧ gets everything a stage DECIDES or writes as prose
      ⑦ gets everything GENERATED from those decisions, plus the
        evidence pointers
      ① gets NOTHING. Nothing a paper run produces is written back into
        the skill: that direction is graduation, and only ② may travel it.

   ── what is DATA and what is a SKILL ─────────────────────────────
      S01-opening … S10-round hold stage DATA: stage.md (contract + craft),
      template.md, and craft .md files. No name: field, not registered.
      Registered skills: the door. ONE, and only one. Everything the
      family used to register is now data the door reads: fn/ verb
      procedures, scripts/ tooling, stage contracts, craft files.

   consulted, never in the chain of command:
     venue/     seven playbook packs, read lazily. NEVER lifecycle verbs.
     _old/      retired history, moved never deleted. NEVER loaded at runtime.

   ────────────── zoom in on the ONE registered skill ──────────────

   tier 1  metadata        name + description     selects the skill, always paid
   tier 2  SKILL.md        the core loop          paid on every invocation
   tier 3  references/     loaded ONLY when its branch is taken
           scripts/        run without consuming reasoning context
           assets/         copied into outputs

   and on any one stage folder: stage.md frontmatter is the CONTRACT the
   door reads; its body is the CRAFT; craft: files load LAST, after the
   phase contract.

   ✗ never in the invocation path, at any tier:
     CHANGELOG.md · feedback/ · migration notes · status reports · design Boards
```

## Content
### The family layers
One door, ten stage data folders, and two consulted shelves.
```text
haipipe-paper/       THE ONE DOOR, and the only registered skill: verbs +
                     stages/index.yml + create-page.py + check-contracts.py +
                     probe/ tooling + ref/ + fn/ (10 verb procedures) +
                     scripts/ (check_structure.sh · diffpdf · project · to-word)
                     + --depth authority
S01-opening/         stage DATA: seed · venue · pitch   (stage.md + template.md each)
S02-work/            stage DATA: resource · claims · narrative
S03-literature/      evidence-page store (route: outward) + template.md +
                     qa-probe-template.md + citation-craft.md
S04-value/           evidence-page store (route: inward) + template.md +
                     qa-probe-template.md + values-craft.md
S05-display/         display stage + draft-craft.md + ref-display/
S06-main/            section-edit stage + revise-place · revise-results ·
                     check-evidence craft files
S07-appendix/        appendix material
S08-present/         empty; paper-slides and paper-poster live in ../display/skills/
S09-build/           the proof-checker/ craft pack; the five build VERBS live in
                     the door's fn/ + scripts/
S10-round/           the round stage (round/stage.md + template.md) +
                     rebuttal-craft.md
venue/               seven playbook packs, consulted never commanded
_old/                retired history, moved never deleted (see _old/README.md)
```
The door resolves ONE stage and hands its S page to `haipipe-page`; the stage folders hold the data the door and the phases read; `fn/folder.md` and `fn/conform.md` scaffold and conform a paper folder. There is no `0-enter/` … `5-present/` bucket layer, no `workers/`, no container pair, and no second orchestrator anywhere in the chain. Canonical tree: `paper/README.md`.

### What every stage runs
The phases are RENTED, not owned. Since thin-paper phase 2 there are no paper phase workers: the four phase contracts, the ten Page Types, the three verbs (CREATE, WORK ON, RUN), and the RUN receipts all live in `board/`, and this folder adds only data.
```text
what ③ owns (the rental)                what ① adds (the data)
─────────────────────────────────────   ──────────────────────────────────────
4 phase contracts  board/page-phases/   craft:    .md files DRAFT/REVISE load
10 Page Types      board/page-types/              LAST (citation · values ·
3 verbs + receipts haipipe-page             display · placement · results
                                                  · evidence · proof-checker/)
                                        checker:  the script CHECK runs before
                                                  judging, declared per stage.md
```
The load order, per phase, is fixed by `board/page-types/haipipe-page-for-stage/SKILL.md` ("checker: and craft:"):
```text
base haipipe-page → for-stage variant → the phase contract → the
stage's craft: files
```
A stage runs the ordered `phases:` list its own stage.md declares; venue declares `[draft, probe, check]`, every other current stage all four.
`gates:` defaults to `[check]`: DRAFT, PROBE, and REVISE run unattended, then ONE human stop.
The unattended run is safe because `probe_depth: 0` caps PROBE at harvesting; passing `--depth N` is the human act that authorizes spend, and it lives in the door.
CHECK runs the declared `checker:` script first (for the probe-consuming stages, `probe/check-probe-cards.sh --stage <key>`); a green gate over a checker FAIL is a defect.
Evidence enters ONLY through PROBE: one `### E<n>` division on an S03/S04 evidence page per Q-executor conversation, each owning one hidden QA-probe under `probes/L|V<nn>-<topic>/<n>-<slug>.md`, whose answers are pointed at QA-bank files in tasks/ and discoveries/, never copied.
This page states the rental and the load order only; the page machinery's own board is the boardform board (`④`).

### What each stage writes, and what appears in the paper
The nine stages of `stages/index.yml`, each row read off its own stage.md tonight.
```text
 stage          phases        writes into ⑧ the paper board                generates in ⑦
 ────────────   ───────────   ──────────────────────────────────────────   ──────────────────
 seed           D P R C       S01-opening/S-Open-Seed.md                   none
 resource       D P R C       S02-work/S-Work-R-resources.md               none
 claims         D P R C       S02-work/S-Work-C-claims.md                  none
                              (the ONLY home of a claim's status)
 venue          D P   C       S01-opening/S-Open-Venue.md                  none
                no REVISE     (the pin lives on this page's state: line)
 pitch          D P R C       S01-opening/S-Open-Pitch.md                  none
 narrative      D P R C       S02-work/S-Work-N-narrative.md               none
 display        D P R C       S05-display/4-display.md                     displays/<unit>/ via the
                              (the brain; commissions the renderers)       four commissioned renderers
 section-edit   D P R C       S06-main/S-<Family>-<unit>-<slug>.md         sections/*.tex, GENERATED
                PER UNIT      one page per section                         from the .md by sync
 round          D P R C       S10-round/S-Round-<unit>-<slug>.md           none
                PER UNIT      one page per dated round                     (it points at a build)
```
Seven of the nine produce nothing in `⑦` at all: their whole product is a page in `⑧`. Only display and section-edit generate manuscript files, and both generate them FROM the page, never the other way round. Paths under ⑧ are relative to the paper's `0-lifecycle/`.

### The anatomy of one unit
Two shapes now, and only one of them is a skill.
```text
a REGISTERED skill (1 of these)          a STAGE DATA folder (9 of these)
<skill-name>/                            SNN-<name>/<stage>/
├── SKILL.md     trigger + shortest      ├── stage.md     frontmatter CONTRACT
│                complete procedure      │                (phases, gates, artifact,
├── references/  loaded only when        │                probe_depth, checker:,
│                its branch is taken     │                craft:) + body CRAFT
├── scripts/     deterministic ops       ├── template.md  parsed by create-page.py
└── assets/      copied into outputs     └── *-craft.md   data the phases load LAST
```
Metadata selects a skill. `SKILL.md` explains the core loop and names exactly which conditional reference to read. Scripts and assets do work without consuming routine reasoning context.
A stage.md has NO `name:` field: it is data the door reads, not a registered skill. Adding a stage is one folder plus one `index.yml` row; no new skill, no version bump, no description edit.

Design Boards, changelogs, feedback archives, migration narratives and status reports do not belong in the live invocation path. If history must be retained, keep it outside the callable skill folder. The compaction evidence flipped sides on 260805 and held through phase 3: the door is 699 lines, and it replaced four routers, a container pair, five build tools and two round skills; an invocation pays the door + the small index + exactly ONE stage.md. Loading all nine stage files would be the regression this layout exists to avoid, and the door's Step 2 forbids it.

### The roster: 1 skill
Measured 2026-08-06 with `find paper -name SKILL.md -not -path '*/_old/*'`, which returns a single path. `ver` is the skill's own `metadata.version`; `lines` is its `SKILL.md`, which is what an invocation of it pays for.
```text
 place        skill                       ver     updated      lines
 ──────────   ─────────────────────────   ─────   ──────────   ─────
 the door     haipipe-paper               0.7.0   2026-08-06     699
 ──────────   ─────────────────────────   ─────   ──────────   ─────
              1 skill                                            699
```
Beside it, loaded only when its branch is taken: `fn/` holds 10 verb procedures totaling 1,908 lines (compile · conform · diffpdf · digest · feedback · folder · probes · project · to-overleaf · to-word), and `scripts/` holds their tooling.

Four things this census says that the 260726 roster could not.

**The roster shrank 36 to 1 across four restructures.** The 260803 SNN move renamed the buckets to the S01 to S10 spine; thin-paper phase 1 dissolved the phase worker skills into stage `craft:` data files plus `board/`'s four phase contracts; thin-paper phase 2 folded `haipipe-paper-enter`, `haipipe-paper-lifecycle`, and `haipipe-paper-stage` into the one door; thin-paper phase 3, on JL's "我们是不是可以先只保留一个 skill", retired the last nine to `_old/phase3-260806/`. Everything removed is in `_old/`, moved never deleted.

**Nothing has reached 1.0.** The one skill is `0.7.0`. No part of this folder has ever been declared stable, and `QF3`'s fresh-agent acceptance has not been passed by the door.

**The two old ownership defects are gone, and the question they asked is now moot.** The rebuttal duplicates retired first (`paper-rebuttal` and `rebuttal-response` to `_old/round-duplicates/`), then `haipipe-paper-rebuttal` itself became `S10-round/rebuttal-craft.md`, a craft file the round stage declares. There is no rebuttal skill left to be the entry. Naming has the same shape: with one skill there is no prefix to keep uniform, and `paper-poster` and `paper-slides` live in `../display/skills/`.

**The invocation cost dropped by an order of magnitude, twice.** 36 SKILL.md files totaled 7,500 lines; ten totaled 2,528; one now totals 699, and a stage run reads it plus one stage.md. The craft did not disappear: it became data, in the seven `*-craft.md` files, the ten `fn/` verb procedures, and the `proof-checker/` pack, each loaded only by the phase or verb that declares it. The nine skills phase 3 retired carried 1,841 SKILL.md lines that no invocation pays any more.

### Which board group rules which skill
This is the `② ──graduates──▶ ①` edge, made addressable. Every group on the design board rules some part of this folder, and a ruling that reaches ✅ has to land somewhere concrete or it has not graduated. This is that target list, so nobody has to guess.
```text
 board page or group           what it rules in ① (or beside it)
 ───────────────────────────   ─────────────────────────────────────────────
 QA1  the folder map           paper/README.md, the family map
 QA2  the skill set            THIS page: the tree layout · the census ·
                               haipipe-paper/SKILL.md's shape
 QA3  the skill board          NOTHING in ①, by design
       it rules the board itself; that is what makes ② deletable
 QA4  the board tool           the ①→③ call sites: build.py · serve.py ·
                               cli/stage.py (rebuild after every write)
 QA5  the probe layer          probe/haipipe-probe binding · the door's
                               probe/ tooling · fn/probes.md
 QA6  the paper scaffold       the door's fn/folder.md + fn/conform.md ·
                               its get-or-create enter path
 QA7  the paper board          the runtime 0-lifecycle/ layout ·
                               S10-round/round/stage.md
 QA8  who owns the page        create-page.py · haipipe-board/cli/stage.py
 QA9  how work is DRIVEN       the door's STAGE step · haipipe-page
                               WORK ON / RUN · haipipe-board/cli/serve.py
 QA10 the prose verb           writing/haipipe-writing/ (⑪, boarded here)
 ───────────────────────────   ─────────────────────────────────────────────
 QC2  the stage contract       stages/CONTRACT.md · index.yml · each
                               SNN stage.md's frontmatter
 QC3-QC3d  the page it writes  SNN */template.md x9 (+ the S03/S04 evidence-page
                               and QA-probe templates) · create-page.py ·
                               haipipe-board/cli/stage.py
 QC4-QC4d  the four phases     board/page-phases/ x4 · each stage.md's
                               craft: and checker: lines · ref/08-stage-gate.md
 QC5  the sentence             citation-craft.md · values-craft.md ·
                               revise-place-craft.md · board/src/body.py
 QC6  the paper skill folder   the S01-S10 spine itself; thin-paper's owner
 QCskill  the mirrors          one Skill-N page per LIVE unit; the roster is now
                               a single card, Skill-0, for the door
 ───────────────────────────   ─────────────────────────────────────────────
 QB0-QB10  the paper board's   the stage data each S page is built from
           S families          (QB5 display · QB6 main · QB9 build · QB10 round)
 QBv  the venue packs          venue/playbook-* x7
 QF2  the contract form        stages/index.yml smallness · the one-stage rule
 QF3  fresh-agent acceptance   the test the door has not passed
```

Three things fall out of reading it as a column.

`QA3` is the only group with no target in `①`, and that is not an omission. It rules the design board itself, which is exactly why `②` can be deleted without breaking anything.

`QA4`, `QA8`, `QA9`, `QC3-QC4d` and `QC5` each name a file in `board/`, which is not inside this folder at all. Those are the rulings that cross a package boundary, and they are the ones most likely to be half-applied: a Law can graduate into the paper skill and quietly not reach the board tool that implements its other half. Thin-paper made this edge heavier, because the four phases themselves now live on the far side of it.

The mirror group `QCskill` used to carry the fold as ⚫ RETIRED banners, one per folded unit. On 260806 JL ruled them out ("we just remove them") and they moved to `_archive/QCskill-retired-260806/` with their link aliases repointed, so the roster shows only live units. After phase 3 that is exactly one card, `Skill-0`, for the door. The 260726 defect this section used to carry, `haipipe-paper-round` contradicting the round ruling, closed twice over: the skill was rewritten to 0.2.0, then became the round stage's own `stage.md`.

### What crosses this folder's edge
```text
 ② the skill board  ──▶ ①    IN, and only this way. A ruling reaches ✅ and its
                             Law is COPIED into the door's SKILL.md, a stage.md,
                             or a ref/ file. Nothing here may read the board back.

 ① ──▶ ⑦ the paper           OUT, only through a stage run. display and
                             section-edit generate manuscript files FROM their
                             pages; the door's build verbs materialize the
                             accepted bundle.
                             No skill file is ever copied into a paper.

 ① ──▶ ⑧ the paper board     OUT, and this is the one people forget. Creating a
                             page is the door's `create-page.py`, which selects
                             the stage and template here, then calls
                             haipipe-board's `cli/stage.py` for the shell. Board
                             owns the filename, Paper owns the Content jobs.
                             Every phase write ends with ③'s build.py rebuild.

 ① ──▶ the wall              NEVER directly. Only PROBE crosses, through an
                             S03/S04 evidence page's E<n> division, its hidden
                             QA-probe under probes/, and clean agents; the
                             answer stays a QA-bank file in tasks/ ·
                             discoveries/, pointed at, never copied. --depth is
                             the human lever that lets a crossing SPEND.
```

### What changes here, and how often
```text
 rarely     the door, the README, this census                   a QA/QC ruling
 per rule   a stage.md's contract fields or craft body          a graduated Law
 per stage  one folder + one index.yml row, no new skill        a new stage
 per venue  a pack under venue/                                 a new outlet
 never      anything naming one paper                           that is ⑦ or ⑧
```

## Aims
- [x] 🗂 Keep the numbered family spine
      The existing top-level organization remains useful and avoids a migration with no user benefit.
- [x] ✂️ Choose progressive disclosure
      One short SKILL.md points directly to conditional references, scripts, and assets.
- [x] 🔭 Say what a stage RUN does, not just which layers exist
      The four phases (rented from `③` since thin-paper), the craft files, and the per-stage write and generate table (260726, JL's ask).
- [x] 🔀 State this folder's three edges
      What comes in from `②`, what goes out to `⑦` and `⑧`, and that only PROBE crosses the wall.
- [x] 🎯 Map every board group to what it rules here
      The graduation edge is addressable: each group names the files a settled Law must land in (JL 260726).
- [ ] 🔗 Carry the cross-package rulings
      QA4, QA8, QA9, QC3-QC4d and QC5 each rule a file in `board/`, outside this folder. Nothing checks that a Law reached both halves.
- [x] 📋 List the roster with versions
      The ONE registered skill after thin-paper phase 3, with its version, date and SKILL.md size.
- [x] 🧠 Rule which rebuttal skill is the entry
      Moot since 260806: `paper-rebuttal` and `rebuttal-response` retired to `_old/round-duplicates/`, then `haipipe-paper-rebuttal` itself became `S10-round/rebuttal-craft.md`. No rebuttal skill remains.
- [x] 🏷 Make the naming uniform
      One registered skill, `haipipe-paper`; `paper-poster` and `paper-slides` moved to `../display/skills/`.
- [ ] ✂️ Make the front door thin
      Move stage craft, comment detail, evidence detail, and output-specific rules to their actual owners. Thin-paper moved the craft out to stage data and the verb procedures out to `fn/`, leaving a 699-line door; the comment and evidence protocols still ride every invocation.
- [ ] 📏 Set a compactness acceptance test
      A fresh agent should identify the entry, stop conditions, and next owner without reading family history.
- [ ] 🧹 Inventory the current paper skills
      Classify every extra file as runtime reference, deterministic script, reusable asset, or design history.
- [ ] 🧠 Rule what a stage may write into `⑦` directly
      Today only display and section-edit generate manuscript files, and only from their page. Whether any stage may write to `⑦` without a page is unstated, and a worker with a plausible reason will eventually do it.
- [ ] 🧪 Trace one request through the layers
      A fresh session should move from Board to stage runner to worker to the same page without another orchestrator.

## States
The ownership map, the anatomy, and the per-stage run map are recorded, and on 260726 a large slice of it was finally APPLIED rather than only argued. Sixteen of the 35 skills were rewritten against `QA6`'s layout ruling in one pass, ordered by which held a live binding rather than by how many stale mentions each had: the four `1-build/` skills first (with `conform` first of those, because it is read-only and once correct it becomes the pass/fail test the other three are written against), then the eight stage contracts, the console, the router and the phase tail. The shared spec `../../paper/phase/REF/paper-folder-anatomy.md` went with them, and it mattered most: its prefix table asserted the exact inverse of the delete test, which is why the family had drifted at all.

The front door was applied too. `haipipe-paper` is now the single thing a human types, and it calls `③` and `⑤` rather than sitting beside them (`QA4`).

The ownership cleanup this face opened with has since landed: four restructures (260803 SNN move, thin-paper phases 1, 2 and 3) folded the routers into one door, dissolved the phase workers into stage craft data files, and then folded the container pair, the five build tools and the two round skills into the door's `fn/` and the round stage. The family now registers exactly ONE skill.

The two zoom levels, family and folder, were separate faces until 260726, when they merged: both answer "what is inside `①`", and splitting them put two of QA's four faces on one quadrant.

Reopened to 🟡 on 260726: the edge map raised a real unruled question, which is whether a stage may write into `⑦` without going through a page.

## Files
- `../../paper/haipipe-paper/SKILL.md`
  The one door (0.7.0, 699 lines), and the family's only registered skill: verbs, the STAGE step, `create-page.py`, `probe/`, `ref/`, `fn/`, `scripts/`.
- `../../paper/haipipe-paper/stages/`
  `index.yml` (read on every invocation), `CONTRACT.md`, `section-kinds.yml`; each row's `dir:` points at a stage folder under `../SNN-*/`.
- `../../paper/S01-opening/ … S10-round/`
  The stage data: nine `stage.md` contracts with their `template.md` and craft `.md` files, plus S09's `proof-checker/` pack.
- `../../paper/_old/phase3-260806/`
  The nine skills phase 3 retired, moved never deleted.
- `../../board/page-phases/`
  The four rented phase contracts; `③`'s, not this folder's.

## Law

- The numbered family spine stays. Each layer owns one responsibility and control flows one way: the front door selects context, the stage runner works one S page, a bounded worker returns to that same page, delivery adapters materialize accepted Content.
- `venue/` is knowledge consulted lazily and never carries a lifecycle verb. `diagram/` holds design Boards and never a runtime contract. Neither is in the chain of command.
- Inside one skill: progressive disclosure. Metadata selects, `SKILL.md` carries the shortest complete procedure and names which conditional reference to read, and everything else loads only when its branch is taken. Design history never sits in the invocation path.
- Nothing in this folder names one paper. A rule that mentions a specific manuscript belongs in `⑦` or `⑧`, not here.

## Log
- 260806 2214 · [REVISE-CC] swept to the 260806 architecture; the roster census replaced, 10 skills to ONE (`haipipe-paper` 0.7.0, 699 lines), with the nine phase-3 retirees named in `_old/phase3-260806/`, the ninth stage `round` added to the write table, and PROBE re-stated as evidence-page E<n> divisions plus hidden QA-probes.
- 260806 0720 · [REVISE-CC] swept to the thin architecture (one door + stage data + board rental); the 260805 ten-skill census is marked as a dated snapshot, with phase 3 (ruled 260806, executing; QC6's Log) collapsing the family to ONE registered skill.
- 260806 0200 · [REVISE-CC] page rewritten to the 0.5.0 one-door architecture (door + stage data + board rental); the bucket-era diagram, 36-skill roster, and 13-worker phase map replaced with the current census

260726 · The map stopped being only a map. 16 skills aligned to `QA6`'s layout in one pass, plus the shared anatomy spec and 90 venue templates; the front door became the single door (`QA4`). The diagram's front-door box now names both dispatches. One correction the pass produced belongs here: measuring per SKILL.md badly understated the work, because `haipipe-paper-stage`'s real debt was in its eight `stages/*/stage.md` contracts, whose paths RESOLVE AT RUN TIME. A stale path in a contract does not read wrong; it writes to the wrong place.

260726 · Added what a stage RUN does (13 workers, the per-stage write/generate table), the roster of 35 skills with versions, and the map of which board group rules which skill. The diagram gained a left column naming the ruling group per layer, on JL's ask. Reopened to 🟡: the edge map raised an unruled question, whether a stage may write into `⑦` without going through a page.
