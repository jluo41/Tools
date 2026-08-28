## 0.3.1 — 2026-08-28

- **A block's task-group home is planned before release** (JL 260828: "这个
  task folder 放哪里,提前规划好"): default `Paper-<Slug>/tasks/B<n>_<slug>/`
  — the paper repo owns its campaign's task groups, so the B<n> grammar
  cannot collide with the host project's `{Letter}{NN}_{slug}` groups and
  the campaign's code/configs/reports travel with the paper. Running inside
  the host project's `tasks/` is a written exception taking that project's
  own grammar. Closes the unpinned-base ambiguity the PNAS board's bare
  `tasks/B1_exam_corpus` cells exposed.

## 0.3.0 — 2026-08-28

- **The Collection page folded in** (JL 260828: "把 roadmap 和 collection 合并到
  一块,不要 collection 了" — the two were one-to-one, plan and result, and the
  lap-L1 field test showed every SD03 edit forcing a mirrored SD02 edit, with
  the three-way string sync as the standing drift risk). This page now carries
  the campaign's PLAN AND INTAKE: the Block Board plus per-block divisions,
  then one lap division per batch brought home, Open last.
- Absorbed from the collection contract, verbatim in force: the Intake law
  (register, never restate; named intake scope), the lap's four register
  blocks (ran/cards/landed/settle), dispatch through this page's `probe/`
  lane, the held-not-answered rule for executors dead before Report
  (halt ≠ null), the settle-verdict adapter with the self-preprint screen,
  and G3's receipt Log row.
- The join tightens: one string on TWO pages (lap landed path = block receipt
  cell, same page; = E-row cite, the Seed). Two pens: this page plans and
  registers; the Seed alone flips.
- Story group is three pages (SD00/SD01/SD02); boards with a separate
  SD03-collection are grandfathered and fold only on explicit request.

## 0.2.0 — 2026-08-28

- **Blocks, jobs, runs** (JL 260828): the campaign cut into BLOCKS — one task
  group per row, the release unit — holding JOBS (task folders) and RUNS
  (configurations), addressed `B<n>T<n>r<n>`; cut by what gates them, not by
  topic; shared sweep axes declared once globally; no release without a run
  count. First used by the PNAS LLMSocialOutcome board (four blocks, 319
  runs).

## 0.1.0 — 2026-08-24

- **Created on JL's 260824 roadmap ruling** ("做完 Ideation 和 Seed 之后完全像
  无头苍蝇" — after ideation and seed nobody knows where to explore): one
  campaign-plan page per paper at `A1-SD-story/SD02-roadmap/`, P2 Roadmap
  (route) of journey 0.5.0's establish loop.
- The Direction Board: eight columns (id · direction · serves · executor ·
  done-when · budget · status · receipt), one row per exploration direction
  (data, model training, results analysis, …), every row serving a named Seed
  E-row — no exploring for exploring's sake, the design family's
  direction-card law.
- Status vocabulary ⬜ proposed → ▶️ released → 🔵 running → ✅ landed /
  🚫 dropped; release is a person's act, row by row; dropped rows never
  deleted.
- Three-pen law: this page plans, the Collection Page dispatches and
  registers, the Seed alone flips E-rows; the join is one QA path in three
  places.

haipipe-page-for-roadmap · Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions
match SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on
`0.x.x` and never reaches `1.0.0` without JL's explicit say-so.

## 0.2.0 — 2026-08-28

- **Re-cut on JL's addressing scheme** (`B1T2r3`): a campaign has three layers
  and they are the task layer's own — BLOCK `B<n>` is a task group, JOB `T<n>`
  is a task folder, RUN `r<n>` is one configuration. One grep-able string now
  addresses a folder, a log line and a receipt at once, so the Direction Board
  became the **Block Board** and rows are ids `B<n>`, not `R<n>`.
- **The block is the RELEASE UNIT, and blocks are cut by what gates them**, not
  by topic: one needing no external access, one spending real budget, one that
  is pure arithmetic over the previous, one touching a single-shot resource.
  The defect this fixes is real and was found in the field: a row spanning an
  elicitation and two gradings could be neither released nor budgeted as one
  thing, and releasing a block that mixes a free job with an expensive one
  forces a person to buy both to get either.
- **Shared sweep axes are declared once, globally** (`d1`, `d2`, …), so a run
  id resolves without a legend and the same index means the same thing in
  every block. A job sweeping more than one axis states the axis ORDER.
- **A block with no run count may not be released**: estimating the size is the
  machine's job, releasing it is the person's, and a campaign nobody has
  counted cannot be budgeted.
- **The row and the task group are the same object seen from two sides**: the
  executor path is `tasks/B<n>_<slug>/`, and `/haipipe-task` is what runs a
  released block. Receipts stay block-level; a roadmap listing runs as receipts
  has become a second task board.
- Each block's division now lists its jobs with run ranges, and hazards that
  would invalidate a block's output are written there BEFORE release.
- Sibling contracts updated to the same vocabulary: the paper door, the
  workflow's G2 line, and the collection page's dispatch language. `R<n>` rows
  on existing boards are grandfathered and migrate only on request.

## 0.4.0 — 2026-08-28

- **MATCH BEFORE SCAFFOLD**, a new executor-column law. Before a block's folder
  is created, the sibling projects' `tasks/` are searched for a group already
  covering the same inputs, and the verdict is written on the block's division
  as REUSE, EXTEND or NEW. A block whose division carries no match verdict may
  not be released.
- The law exists because the failure is observed, not hypothesised: a block was
  scaffolded to recompute arm-level outcomes from raw parquet while a sibling
  project's task group had produced the same arm-effectiveness analysis months
  earlier. Nobody looked, because nothing required looking.
- This is the probe family's match-before-dispatch law applied one layer down.
  Probe matches QUESTIONS against a QA bank; a roadmap block matches INPUTS
  against the workspace's task groups. Same failure, same remedy.
