# The stage engine: ten skill folders become stage data
state: 🔴 OPEN
owner: JL
method: lay the port out from paper's live engine, then put the three cutover decisions to JL as Decision Now rows

## Opening
How does round 3 port paper's stage engine to the application family: what is a stage as data, what does the index resolve, and in what order do the ten per-stage skills cut over?
On the paper side a stage is one data file, stage.md, and a small index.yml says which one to load.
On the application side each of the ten stages, seed through section-edit, is still its own skill folder.
This page lays the port out and puts its three decisions to JL; it rules on nothing.

**A stage as data**: paper's venue stage is the single file stages/2a-venue/stage.md, whose frontmatter declares the contract (phases [draft, probe, check], gates, artifact) and whose body carries the craft.
Nothing else loads when venue runs.

**The precedent**: paper already ran this cutover, and today all eight of its index rows read migrated: true.
While a row was false, the router handed off to the named legacy skill, so unported stages never broke.
The stage contract itself is settled as QC2@paper and the phase flow as QC4@paper; this page ports their results and does not reopen them.

**What the application adds**: three things paper's contract form has no field for: venue gating (stages 3 to 5 fire only when the pinned venue requires them), settlement depth (light | medium | full on the 1c claim ledger), and ladder gate batching (one combined gate at 1d for light venues, four gates for full).
Part 1 proposes a home for each.

**Why it matters**: ten stage skills carry ten copies of the same phase-loop plumbing, so one spine change is ten edits that drift apart.
Paper collapsed that into one router plus stage data, guarded by one rule: never load the other stages, because loading all eight at once measured as a 7.5x context regression.

## Diagram
**The port at a glance**: entry, stages, and gating today, and after the port.

```text
📦 TODAY
  🚪 entry     haipipe-application-lifecycle · routes stages + owns the ladder sweep
  🧰 stages    10 per-stage skill folders · seed … section-edit
  🧭 gating    STATUS.md rows · venue · stages_skipped · claims_settlement

🎯 PROPOSED
  🚪 entry     one stage router · stage key first
  🗂 stages    stages/<order>-<key>/stage.md ×10 · loaded one per invocation
  📇 resolver  stages/index.yml · migrated: + legacy_skill: per row
  🧭 gating    venue gate · settlement depth · gate batching as contract fields
```

## Content

### 1 · 🗂 A stage as data
**One stage folder**: the two files that describe a stage, and when each is read.

```text
📇 stages/index.yml                one row per stage · read on EVERY invocation
🗂 stages/<order>-<key>/stage.md   contract (frontmatter) + craft (body) · read when picked
⛔ guard                           never load the other stages' stage.md files
⚖️ precedent                       QC2@paper stage contract · QC4@paper phase flow
```
📌 This part says what a stage is once it is data, taken from paper's live layout, and names the ten files the port creates plus the three fields the application must add.

Paper deleted its eight per-stage skills; every stage is now one stages/<order>-<key>/stage.md whose frontmatter is the contract and whose body is the craft.
The contract's required core is 24 fields, grouped as identity, board, execution, product, evidence, graph, and closing (stages/CONTRACT.md).
The port creates the same tree with ten directories: 0-seed, 1a-descriptions, 1b-themes, 1c-claims, 1d-advice, 2a-venue, 2b-pitch, 3-narrative, 4-display, 5-section-edit.
This stages/ tree is engine data inside the skill; the intervention folder contract (0-lifecycle/2-venue/, 2-pitch/, and the rest) does not change.

#### 1.1 · What carries over unchanged
(the paper core fields the application contract keeps as they are)
The application stage skills already run DRAFT, PROBE, REVISE, CHECK through the shared 2-phase workers, so `phases:`, `gates:`, and `probe_depth:` map straight across.
`artifact:`, `template:`, and `sections:` map to the existing stage docs, N-<stage>.md plus _LOG in each stage folder.
`probes:` and `q_id_pattern:` map to the flat 1-probes/ pool the stages already raise their questions into.

#### 1.2 · The three application deltas
(what the stage data must carry that paper's 24-field core has no slot for)
Venue gating: stages 3 to 5 fire per venue, read from STATUS.md's stages_skipped row, so the narrative, display, and section-edit contracts need a declared skippable-by-venue field where paper stages are never skipped.
Settlement depth: the venue writes claims_settlement (light | medium | full), which sets how much of the 1c ledger must settle before draft, so the claims contract's done_criteria must read that row rather than hardcode one bar.
Ladder gate batching: the venue's depth batches the rung gates (light: one combined gate at 1d; medium: 1c plus 1d; full: four), so a rung's `gates:` is venue-scaled where paper's default is a constant [check].

### 2 · 📇 What the index resolves
**The resolve step**: the one small file read every time, and the two paths out of a row.

```text
📇 row fields        key · order · dir · triggers · migrated (+ legacy_skill while false)
✅ migrated: true    read stages/<dir>/stage.md · that one file only
🚧 migrated: false   Skill(legacy_skill) · hand off and stop
```
📌 This part says what the index owns, why it stays small, and where the entry verb above it lands.

The index holds only what a router needs to choose: key, order, dir, triggers, and the migrated flag; everything else about a stage lives in the stage.md loaded only when picked (stages/CONTRACT.md).
It is read on every invocation, including ones that turn out to be about something else, which is why nothing else belongs in it.
The migrated flag is the cutover instrument: a false row hands off to its legacy skill and stops, so users see identical behavior on unported stages for the whole transition.
The application index opens with ten false rows, each naming its handoff: seed to haipipe-application-seed, descriptions to haipipe-application-descriptions, and so on through section-edit to haipipe-application-section-edit.

#### 2.1 · The router above the index
(where the entry verb lives, and what happens to haipipe-application-lifecycle)
Paper's entry is /haipipe-paper-stage with the stage key first, and each invocation is exactly one stage; the router has no sweep verb.
The application's entry today is haipipe-application-lifecycle, which routes single stages and also owns the ladder verb: one 1a to 1d sweep with venue-scaled gate batching.
The sweep has no paper equivalent to inherit, so the port must give it an owner; that is the third Decision Now row.

### 3 · 🔁 The cutover order
**Three candidate orders**: which cohort of rows flips migrated: true first.

```text
🪜 A ladder first   0-seed + 1a-1d · proves sweep + gate batching earliest
🐢 B tail first     3-narrative + 4-display + 5-section-edit · least traffic
📦 C all at once    all ten in one push · no mixed period · one large review
♻️ retire rule      a skill folder retires when its stage.md lands + row flips
```
📌 This part states the retirement rule and lays out the three orders JL can choose between.

The unit of cutover is one index row: a per-stage skill folder retires when its stage.md lands, its row flips to migrated: true, and its legacy_skill handoff is deleted.
Because a false row keeps working through its legacy skill, the order is a scheduling choice, not a safety one; what it decides is where a port mistake surfaces first and which delta is proven earliest.
Ladder first (0-seed plus 1a to 1d) fronts the hardest delta: the four rungs share the sweep and the venue-batched gates, so the first cohort exercises gate batching and settlement depth at once.
Tail first (3-narrative, 4-display, 5-section-edit) fronts the safest cohort: light venues skip all three stages, so a mistake hits the fewest live runs, but the sweep stays unproven until last.
All at once removes the mixed period and takes one review, at the price of one large change with no early warning from a small cohort.
2a-venue and 2b-pitch sit in the middle cohort under either phased order.

## Aims

### A1 · 🗂 A stage as data
- A1.1 · The application stage contract form is written: the paper core fields that carry over, plus a declared home for each of the three deltas.
  **Done when:** A contract form names every required field, and venue gating, settlement depth, and ladder gate batching each have one field that carries them.
- A1.2 · Ten stage.md files exist under stages/, one per lifecycle stage.
  **Done when:** stages/0-seed through stages/5-section-edit each hold a stage.md that passes a contract check equivalent to paper's check-contracts.py.

### A2 · 📇 What the index resolves
- A2.1 · stages/index.yml exists with ten rows, each carrying migrated: and, while false, a legacy_skill handoff that resolves.
  **Done when:** Every row's dir exists and every migrated: false row names a per-stage skill that still exists.

### A3 · 🔁 The cutover order
- A3.1 · Every per-stage skill folder is retired in the ruled order.
  **Done when:** All ten index rows read migrated: true and no per-stage skill folder remains under application/_old/1-lifecycle/.

### P · Page-level
- P1 · JL has ruled the three Decision Now rows.
  **Done when:** Each row is closed with its ruling recorded in ## Law and the change in ## Log.

## States

### Decision Now
- [ ] 🗣 Adopt the stage-engine port for the application family?
      📍 `Part` 1 and 2, the design this row puts in motion
      🔔 `Why now` round 3 is the porting round, and the two rows below assume an answer here.
      ⭐ `A ·` port it: stages become data under one router and the ten skill folders retire as their stage.md files land; CC recommends A because paper has run this layout since its own cutover and the migrated flag keeps every unported stage working.
      `B ·` keep the ten skill folders: no engine, and the three deltas stay in STATUS.md rows and orchestrator prose.
      🛑 `Blocks` the two rows below and all A1, A2, A3 work.
      🤖 `If nobody answers` B stands by inertia: the skill folders keep running unchanged.

- [ ] 🗣 In what order do the ten per-stage skills cut over?
      📍 `Part` 3, the three candidate orders and the retirement rule
      🔔 `Why now` the first cohort sets the pattern the remaining rows copy.
      ⭐ `A ·` ladder rungs first: 0-seed plus 1a to 1d flip first, proving the sweep, gate batching, and settlement depth in the first cohort; CC recommends A because the ladder is where the application differs most from paper, so a port error surfaces earliest there.
      `B ·` tail first: 3-narrative, 4-display, and 5-section-edit flip first, so a mistake hits the fewest live runs but the sweep stays unproven until last.
      `C ·` all at once: all ten rows flip in one push, with no mixed period and one large review.
      🛑 `Blocks` which stage.md files A1.2 drafts first, and the retirement schedule in A3.1.
      🤖 `If nobody answers` A, the ladder cohort, once the row above is answered with adopt.

- [ ] 🗣 Does haipipe-application-lifecycle stay above the engine as the ladder sweep orchestrator?
      📍 `Part` 2.1, the router above the index
      🔔 `Why now` paper's router has no sweep verb, so the 1a to 1d sweep needs an owner on day one of the port.
      ⭐ `A ·` keep it: the lifecycle skill stays as the sweep orchestrator above the engine and the engine owns single-stage runs; CC recommends A because the sweep and its gate batching are working behavior with nothing in paper to inherit them.
      `B ·` retire it too: the engine's router grows a ladder verb and the orchestrator folder goes the way of the ten.
      🛑 `Blocks` nothing until the first ladder rung cuts over; after that, a sweep with no owner blocks the ladder cohort.
      🤖 `If nobody answers` A: keeping the orchestrator costs nothing, and folding it in stays possible later.

### A1 · 🗂 A stage as data
- ⬜ A1.1 · Not started; the paper form (stages/CONTRACT.md) is read, and no application form is drafted.
- ⬜ A1.2 · Not started; no stages/ tree exists in the application family.

### A2 · 📇 What the index resolves
- ⬜ A2.1 · Not started; the ten proposed rows exist only on this page.

### A3 · 🔁 The cutover order
- ⬜ A3.1 · Not started; all ten per-stage skill folders are live.

### P · Page-level
- 🧠 P1 · Waiting on JL; the three Decision Now rows above are open.

## Files

### Engines
- `../../../../application/_old/1-lifecycle/haipipe-application-lifecycle/SKILL.md`
  The orchestrator the engine augments or replaces; the third Decision Now row decides its fate, and it is the first file to edit once JL rules.

### Input files
- `../../../../paper/haipipe-paper-workflow/SKILL.md`
  The paper router this page ports: stage resolution, one-stage-one-file loading, and the migrated handoff.

## Glossary
- 🏗 **stage engine**: paper's layout where one router reads stages/index.yml and loads a single stages/<dir>/stage.md per invocation; the thing this page ports.
- 🪜 **the ladder**: the application's venue-free evidence rungs, 1a-descriptions to 1b-themes to 1c-claims to 1d-advice; the ladder verb runs them as one sweep.
- 🚧 **migrated flag**: the index row field that says whether a stage has cut over; false hands off to the row's legacy_skill and stops.
- 📏 **settlement depth**: the venue-written claims_settlement row (light | medium | full) saying how much of the 1c claim ledger must settle before draft.

## Log
260802 · Page opened; the port laid out from paper's router, index, and contract form, with three decisions put to JL.
