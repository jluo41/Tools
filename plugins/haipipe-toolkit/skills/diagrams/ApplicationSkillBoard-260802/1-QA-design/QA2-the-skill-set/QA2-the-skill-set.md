# The skill set: what ships
state: 🔴 OPEN
owner: JL
method: count the tree from each SKILL.md frontmatter, group by the README's layers, judge the collapse against QA2@paper

## Opening
What does the Application family ship today, and which of it does round 3 collapse into stage data?
On disk the family is 23 callable skills plus 8 venue packs under `skills/application/`.
Ten of the 23 are per-stage skills in `1-lifecycle/` that each restate one lifecycle shape.
The paper family already folded its per-stage skills into data files under one engine.
This page counts the roster, with versions, and puts that collapse in front of JL.

**What the words mean**: A layer is one top-level folder of the family tree, such as `1-lifecycle/` or `2-phase/`.
A stage orchestrator is a user-facing skill that owns one lifecycle stage's deliverable, such as `haipipe-application-claims` owning the 1c claim ledger.
A phase worker is an internal skill every stage drives through DRAFT, PROBE, REVISE and CHECK.
Collapsing into stage data means a stage stops shipping its own SKILL.md and becomes a `stages/<dir>/stage.md` file that one engine reads.

**The precedent**: QA2@paper is this same page on the paper board.
Its roster shows the shape after the move: one `haipipe-paper-stage` engine driving eight per-stage contracts kept as data files.

**Why it matters**: Ten SKILL.md files restating one shape drift ten ways, and a rule fixed in one rung silently misses the other nine.
QA2@paper also sets the bar for closing this page: a settled ruling has to land in concrete files, not stay as architecture.

**What this page does not own**: The internals of the phase workers, the contents of the venue packs, and the collapse migration itself.
This page counts what ships and holds the one decision about it.

## Writing Style
**Numbers from disk**: Every version and date on this page is copied from a SKILL.md frontmatter (`metadata.version` and `last_updated`), never from memory or from a README claim.

**Names in full**: A skill is named with its full `haipipe-application-` prefix in backticks, because the prefix is how the family is discovered.

**The candidate mark**: 🔻 marks a round-3 collapse candidate wherever it appears on this page, and nothing else uses that mark.

## Diagram
**The page at a glance**: what ships, what round 3 would move, and who rules it.

```text
 📦 ships       23 skills across 6 layers · 8 venue packs beside them
 🔻 candidates  10 per-stage skills, all inside 1-lifecycle/
 ⚙️ proposal    one haipipe-application-stage engine + stage.md ×10 (option A)
 🗣 decision    JL rules it in States · Decision Now
```

## Content
### 1 · 📦 The roster: 23 skills and 8 packs
**Counts by layer**: the family tree as it sits on disk today.

```text
 🚪 door         1 skill    the router and console front door
 0️⃣ 0-enter      2 skills   enter · round
 1️⃣ 1-lifecycle  11 skills  1 orchestrator + 10 per-stage 🔻
 2️⃣ 2-phase      4 skills   draft · probe · revise · check
 3️⃣ 3-deliver    4 skills   artifact · review · claim-audit · deploy
 4️⃣ 4-iterate    1 skill    post-deploy A/B refinement
 🎒 venue/       8 packs    knowledge, not stages
```
📌 This part is the count itself: every callable skill with its version, plus the venue packs beside them, read from disk on 260802.

The layer grouping follows the Skill-tree layout in the family README, which is the canonical structure file.

#### 1.1 · The 23 callable skills
(the versioned roster, one row per SKILL.md frontmatter on disk)
**The roster, grouped by layer**: ver is the skill's own `metadata.version`, updated is its `last_updated`.

```text
 layer         skill                              ver      updated
 ───────────   ────────────────────────────────   ──────   ──────────
 🚪 door       haipipe-application                0.6.10   2026-07-19
 0-enter       haipipe-application-enter          0.2.3    2026-07-19
               haipipe-application-round          0.1.1    2026-07-06
 1-lifecycle   haipipe-application-lifecycle      0.4.4    2026-07-19
   🔻 stage    haipipe-application-seed           0.6.1    2026-07-19
   🔻 stage    haipipe-application-descriptions   0.2.6    2026-07-19
   🔻 stage    haipipe-application-themes         0.2.7    2026-07-19
   🔻 stage    haipipe-application-claims         0.7.6    2026-07-19
   🔻 stage    haipipe-application-advice         0.1.9    2026-07-19
   🔻 stage    haipipe-application-venue          0.3.4    2026-07-19
   🔻 stage    haipipe-application-pitch          0.5.4    2026-07-19
   🔻 stage    haipipe-application-narrative      0.5.4    2026-07-19
   🔻 stage    haipipe-application-display        0.4.8    2026-07-19
   🔻 stage    haipipe-application-section-edit   0.5.4    2026-07-19
 2-phase       haipipe-application-draft          0.1.5    2026-07-19
               haipipe-application-probe          0.3.2    2026-07-19
               haipipe-application-revise         0.1.1    2026-07-19
               haipipe-application-check          0.4.2    2026-07-17
 3-deliver     haipipe-application-artifact       0.3.1    2026-07-17
               haipipe-application-review         0.1.1    2026-07-06
               haipipe-application-claim-audit    0.1.2    2026-07-17
               haipipe-application-deploy         0.1.1    2026-07-06
 4-iterate     haipipe-application-iterate        0.2.0    2026-07-17
 ───────────   ────────────────────────────────   ──────   ──────────
               23 skills · 🔻 ×10 = round-3 collapse candidate
```

The ten 🔻 rows are the per-stage skills of `1-lifecycle/`: the nine numbered stage folders plus `haipipe-application-venue`, which pins the modality between the ladder and pitch.
The orchestrator `haipipe-application-lifecycle` is the eleventh skill in that layer and is not a candidate; it is the seat the engine proposal builds beside.

#### 1.2 · The eight venue packs
(the knowledge folders beside the skills, counted apart because they are not callable)
Under `venue/` sit eight packs: sms, email, push, reminder, checklist, dashboard, report, and ui-card.
Each is a README plus a style-profile, with a shared `_SCHEMA.md` beside them, and the family README calls them knowledge, not stages.
They carry no version and no trigger, so they ship with the family without being part of the 23.

#### 1.3 · What the versions say
(the three facts the roster states that no prose above it did)
Nothing has reached 1.0: the highest version anywhere is `haipipe-application-claims` at 0.7.6, and seven skills are still 0.1.x.
Sixteen of the 23 last moved on 2026-07-19 and nothing has moved since, so this count is stable rather than mid-flight.
The naming is uniform: all 23 carry the `haipipe-application-` prefix, which QA2@paper could not say of its family, where four skills dropped the prefix.
The ladder's wear is uneven: `haipipe-application-claims` sits at 0.7.6 while `haipipe-application-advice` sits at 0.1.9, because the 1d rung was renamed from `1d-principles` to `1d-advice` only on 2026-07-09 and its skill is weeks old.

### 2 · 🔻 The round-3 collapse
**Before and after the collapse**: the shapes option A trades between.

```text
 🔻 today      1-lifecycle/ = 1 orchestrator + 10 per-stage SKILL.md
 ✅ option A   1-lifecycle/ = orchestrator + 1 engine + stage.md ×10
 🧭 precedent  paper: haipipe-paper-stage + 8 stage contracts (QA2@paper)
```
📌 This part names what round 3 would move, the precedent it copies, and the files a yes must land in.

#### 2.1 · What collapses and what stays
(the ten candidates, and the thirteen skills the move does not touch)
The ten candidates are all of `1-lifecycle/` except the orchestrator: seed, descriptions, themes, claims, advice, venue, pitch, narrative, display, and section-edit.
Each would stop shipping a SKILL.md and become one `stages/<dir>/stage.md` data file under a new `haipipe-application-stage` engine.
The door, the 0-enter pair, the four phase workers, the four deliver skills, iterate, and the lifecycle orchestrator stay callable, so the family lands at 14 skills.
The venue packs are untouched: they are knowledge the aligned stages consult, whichever form the stages take.

#### 2.2 · The precedent: paper already made this move
(the shape on the paper side, which round 3 would copy)
The paper family took this shape in its 260719 refactor: per-stage skills became stage contracts under one runner.
QA2@paper's roster shows the result, `haipipe-paper-stage` at 0.6.0, and its Files row carries `stages/index.yml`, the eight contracts, and `CONTRACT.md`.
The application README declares the two families structural twins, same spine, same phases, same probe door, so a shape proven on one side is the default proposal for the other.

#### 2.3 · A yes must land in files
(the graduation rule, and the concrete landing list for option A)
QA2@paper states the closing rule this page inherits: a ruling that reaches ✅ has to land somewhere concrete or it has not graduated.
For option A the landing list is: a new `1-lifecycle/haipipe-application-stage/SKILL.md`, ten `stages/<dir>/stage.md` files, the ten retired skill folders removed from the tree, the README's Skill-tree layout rewritten, and the door's router table repointed.
A ruling recorded only as architecture prose on this board would be exactly the drift that rule exists to stop.

## Aims
### A1 · 📦 The roster
- A1.1 · The roster on this page matches the tree on disk.
  **Done when:** Every version in Part 1 equals the `metadata.version` in that skill's SKILL.md frontmatter, and the 🔻 rows count exactly ten.

### A2 · 🔻 The collapse
- A2.1 · JL rules the round-3 collapse question.
  **Done when:** The Decision Now row is answered, the ruling sits in a dated Law entry, and this Aim's State names the chosen option.
- A2.2 · The ruling lands in concrete files.
  **Done when:** The chosen option's landing list from Part 2.3 exists on disk, or the ruling records why nothing moves.

## States
### Decision Now
- [ ] 🗣 Do the ten 1-lifecycle stage skills collapse into stage data under one engine in round 3?
      📍 `Part` 2 · the round-3 collapse
      🔔 `Why now` round 3 is being scoped and the family has not moved since 2026-07-19, so the collapse can land before new stage edits pile up
      ⭐ `A ·` collapse all ten: add `haipipe-application-stage`, write ten `stages/<dir>/stage.md` files, retire the ten skill folders, rewrite the README and the door's routing; CC recommends A because ten SKILL.md files restating one shape drift ten ways and the paper engine has already carried this exact move
      `B ·` keep the ten callable and share their common shape through one ref file; cheaper this round, and the ten-way drift risk stays
      `C ·` defer past round 3 until the paper engine has survived a full paper cycle; nothing moves this round
      🛑 `Blocks` the round-3 restructure of `1-lifecycle/`; the roster in Part 1 stays correct either way
      🤖 `If nobody answers` C in effect: the tree stays as counted and the ten stay callable

### A1 · 📦 The roster
- ✅ A1.1 · Met on 260802; the 23 frontmatters were read for this page, the table carries their versions verbatim, and the 🔻 rows count ten.

### A2 · 🔻 The collapse
- 🧠 A2.1 · Waiting on JL; the Decision Now row above carries the three options.
- ⬜ A2.2 · Not started; it opens the moment A2.1 is answered.

## Files
### ⚙️ Engines
- `../../application/haipipe-application/SKILL.md`
  The door; its frontmatter opens the roster at 0.6.10, and its router table is on Part 2.3's landing list.
- `../../application/1-lifecycle/haipipe-application-lifecycle/SKILL.md`
  The spine orchestrator, 0.4.4 in the roster, and the seat the proposed engine would sit beside.

### 📥 Input files
- `../../application/README.md`
  The canonical structure file; Part 1's layer grouping and the 1d rename history follow it.
- `../PaperSkillBoard-260725/1-QA-design/QA2-the-skill-set/QA2-the-skill-set.md`
  QA2@paper: the precedent roster, the engine shape Part 2.2 cites, and the graduation rule Part 2.3 inherits.

## Glossary
- 📚 **stage orchestrator**: the user-facing skill owning one lifecycle stage's deliverable, such as `haipipe-application-claims` owning the 1c claim ledger.
- ⚙️ **phase worker**: an internal skill a stage drives; the four are draft, probe, revise, and check, and a user never invokes them directly.
- 🎒 **venue pack**: a knowledge folder under `venue/`, a README plus a style-profile, consulted by venue-aligned stages and never a lifecycle verb.
- 🗂 **stage data**: a `stages/<dir>/stage.md` contract file one engine reads, replacing a per-stage SKILL.md; the paper family's current shape.
- 🔁 **round 3**: the rework pass this board is scoping; this page marks which skills that pass would collapse.

## Log
260802 · Page opened: counted 23 skills and 8 venue packs from the frontmatters and the README, marked the ten 🔻 collapse candidates, and raised the collapse decision for JL.
