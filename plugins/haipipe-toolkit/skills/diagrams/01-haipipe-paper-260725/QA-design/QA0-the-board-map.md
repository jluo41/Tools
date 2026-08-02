# The board map: which group answers which question

state: 🟡 PARTIAL · the four layers and the delivery order are ruled; five routing gaps are open and the cold read has never run
owner: JL
method: start from the required delivery, map it through skill-first Engine routes, then record bounded executions as evidence

## Opening

How do you read this board?
Four groups, and each owns one question.
`QB5` says a paper owes its reader a figure, `QC1` says which skill makes one, `QF1` records the run that did.
Start in the wrong one and every answer reads as an opinion, because the page that owns the fact is elsewhere.
This page fixes the order and says what each group owns.

**Where this page sits**: This is the entry face, and it is the only page whose subject is the board itself rather than the paper.
`QA1` takes over at the next question, which is where a given file belongs among the folders.
Everything else on the board is inside one of the four groups this page names.

**Why the order is a ruling and not a preference**: Delivery is the reader-facing specification, so it can be written before any skill exists to satisfy it.
Engine is skill-first rather than stage-first, because one skill serves several deliveries and one delivery needs several skills.
Execute comes last because it can only report on a route that already exists.
Reversing any pair makes a page assert something the page it depends on has not decided yet.

**What this page does not own**: The delivery order it prints belongs to Delivery, the skill crosswalk to `QC1`, and every run record to `QF1`.
This page states the reading order and stops; a fact stated twice drifts.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4@boardform`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Name a group by what it ANSWERS, never by its letter alone**: a bare group letter means nothing to a reader who arrived from one link.
Write "Delivery, what the reader gets" the first time in any division.

**Never restate a fact another group owns**: the delivery order, the skill crosswalk and the run records each have an owning page.
Cite the id and stop, because a copy here goes stale the day the owner changes.

**A count of pages or groups belongs in States, never in Content**: this page has already carried "53 Page routes" past two regroupings.
Content states what is true by design; States states what is true today and is expected to move.

## Diagram

**The reading order**: four groups, four questions, one direction.

```text
 🧭 QA · DESIGN     what the Paper system IS, and who owns its boundaries
        │ shapes
        ▼
 📦 QB · DELIVERY   what readers and collaborators RECEIVE
        │           Opening → Work → Literature → Value → Display
        │           → Main → Appendix → Present → Build → Round
        │ served by
        ▼
 ⚙️ QC · ENGINE     which reusable route MAKES each delivery
        │ demonstrated by
        ▼
 🧪 QF · EXECUTE    what actually RAN, passed, failed, or reopened work

 🔒 the order is a dependency, not a preference: Execute can only report on
    a route Engine already declares, for a delivery QB already specified
```

## Content

### 1 · The four layers

**Who answers what**: the question each group owns, and the one it must never answer.

```text
 🗂 GROUP        ❓ ANSWERS                        🚫 NEVER ANSWERS
 ───────────     ──────────────────────────       ─────────────────────────
 🧭 QA Design    what the system is · who owns    what a reader receives
 📦 QB Delivery  what the reader gets · the       which skill produces it
                 human decision it is fit
 ⚙️ QC Engine    which route may produce it       whether it ran
 🧪 QF Execute   what one bounded run did          whether the design is right

 ↩️ a failed run REOPENS the owning Delivery or Engine page
 🚫 a failed candidate never becomes an implicit promotion
```

🧭 Establishes the four questions, their fixed order, and the one direction a failure travels.

#### 1.1 · Delivery is a specification, so it comes before any skill
(it can be written and accepted while nothing yet exists to satisfy it)
Delivery owns the desired artifact, its canonical content, and the human decision that it is fit to hand off.
Its reading order is not an execution graph and never renumbers a lifecycle stage.

#### 1.2 · Engine is skill-first, not stage-first
(one skill serves several deliveries, and one delivery needs several skills in sequence)
The Engine map links to authority and never copies or replaces it.
A skill card states its trigger, the delivery content it serves, what it reads, what it may write, its handoff, its refusal boundary, and its Execute evidence.

#### 1.3 · Execute is one bounded attempt, and a failure travels upward
(it records what happened; it never becomes a second place where design is decided)
One run turns one Delivery target through one Engine route on a named fixture or paper, producing an artifact, candidate, observation, gate result, or receipt.
Tests, compile checks, gates and fresh-agent observations are ways of gathering that evidence, never a separate authoring layer.
Failure reopens the owning Delivery or Engine page.

### 2 · The delivery order, and who ruled it

**Ten concerns in reader order**: the sequence Delivery owns, printed here for orientation only.

```text
 Opening ▸ Work ▸ Literature ▸ Value ▸ Display ▸ Main ▸ Appendix
         ▸ Present ▸ Build ▸ Round

 📍 Venue sits INSIDE Opening        📊 Present includes slides and posters
 🏦 Work grows the banks by probe    📦 Build also owns diffusion/distribution
 🔁 Round is a BATCH, which is why it is not called Response

 ⚠️ this is the READING order. Engine dependencies and stage revisits are
    declared explicitly and never inferred from group adjacency
```

📦 Establishes the accepted concern order and the four naming rulings inside it.

#### 2.1 · The order is JL's ruling, and the sequence is the whole of it
(each of the four naming decisions fixed a word that was doing two jobs)
Venue moved inside Opening, Work took the position immediately after it, Present kept slides and posters, and Build absorbed diffusion and distribution.
Response became Round because the unit is a batch rather than a single reply.

#### 2.2 · Three series sit below the ten, and they are not concerns
(they say what a delivery rule APPLIES TO, which is a different axis)
`QB11` holds rules whose unit is a whole section, `QB12` one sentence, and `QB13` one float.
A concern says what the reader gets; a series says what a rule is about, so the two never compete for the same page.

### 3 · Source and generated

**Two trees, one board**: what a person edits, and what a build writes.

```text
 ✏️ BOARD-FOLDER · edit this        🌐 BOARD-WEBPAGE · never hand-edit
 ──────────────────────────         ─────────────────────────────────
 board.md          the registry  ━▶ board/index.html
 QA-design/*.md    one page      ━▶ board/QA.html      one per group
 QB-delivery/*.md  per file      ━▶ board/QA/<page>.html
                                 ━▶ board/_assets/     shared css + js

 🔁 build.py reroots every source-relative link, image and PDF per depth
 🗑 board.html is retired: Index, Group and Page are the one surface
```

🌐 Establishes which tree is authored and which is derived, so nobody edits the wrong layer.

#### 3.1 · Identity survives a regrouping, and aliases are how
(a page keeps its meaning when its group letter changes)
Every live page id matches its current group, and an old id with no collision stays a declared alias in `board.md`'s `## Links`.
The former Engine `QB*` and `QC*` names collided with the new Delivery and Engine series, so their references were migrated to current ids rather than left ambiguous.

## Aims

### A1 · 🧭 The four layers
- A1.1 · The board is read Design, Delivery, Engine, Execute, and each group answers only its own question.
  **Done when:** no page states a fact another group owns, and each group's pages answer only the question named in `### 1`.
- A1.2 · A failed run reopens the page that owns the route rather than settling anything itself.
  **Done when:** every Execute record names the Delivery or Engine page a failure reopens.

### A2 · 📦 The delivery order, and who ruled it
- A2.1 · The ten concerns are in the accepted reader order with the four naming rulings applied.
  **Done when:** `QB1` through `QB10` carry the ruled order, and no page calls Round "Response" or places Venue outside Opening.
- A2.2 · Every Delivery overview names an Engine route and its Execute evidence.
  **Done when:** each of `QB1`-`QB10` names a route and a run, or an explicit gap, and none claims a route that does not exist.
- A2.3 · Every skill page states what it Serves and what proves it.
  **Done when:** each `Skill-<n>` page carries a Serves line and an Execute-evidence line.
- A2.4 · A skill earns its own page only when its responsibility cannot stay a leaf of an existing route.
  **Done when:** `haipipe-paper-deliver` and `haipipe-paper-project` have each been audited against that test and the verdict recorded.
- A2.5 · An Execute record exists only where a route is runnable.
  **Done when:** Present and Round remain visible as delivery gaps until each has a callable route and one bounded run.

### A3 · 🌐 Source and generated
- A3.1 · The authored tree and the generated tree are separable, and nothing hand-edits the second.
  **Done when:** `check.py` verifies the generated Index, Group, Page, assets, fragments and local resources with zero findings.

### P · 🏁 Page-level
- P1 · A fresh reader can navigate the reorganized board without being taught it.
  **Done when:** a cold-read agent names which group owns a given question, for five questions drawn from different groups, without opening this page twice.

## States

### A1 · 🧭 The four layers
- ✅ A1.1 · The registry reads Design, Delivery, skill-first Engine, then Execute evidence. The 260801 consolidation folded 16 historical groups into the four.
- 🔨 A1.2 · Stated in `## Law` and practised by the one real record: the MISQ Main-1 candidate names its blocker. Whether every future record will is not enforced.

### A2 · 📦 The delivery order, and who ruled it
- ✅ A2.1 · Ruled by JL on 260729 and applied. `QB11` through `QB13` were added on 260802 as series rather than concerns, which left the ten untouched.
- ⬜ A2.2 · Not started. Do it one group at a time, so no page claims a route or run that does not exist.
- ⬜ A2.3 · Not started. The initial skill cards become the first Engine route, never a new authority layer.
- ⬜ A2.4 · Not started.
- ⬜ A2.5 · Not started. Present and Round are the two currently visible as gaps.

### A3 · 🌐 Source and generated
- ✅ A3.1 · `board.md` declares both trees and the strict checker verifies the generated side.

### P · 🏁 Page-level
- ⬜ P1 · Never run. The board has grown from 53 pages to 63 since the reorganization it would have judged.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `board.md`
  The registry: the spine, the close condition, the page roster, and the `## Links` alias table that keeps old ids resolving.
- `QC-engine/QC1-delivery-skill-map.md`
  The many-to-many Delivery × Skill crosswalk this page points at and does not hold.
- `QF-execute/QF1-execution-map.md`
  The run records and their failure-to-reopen links.

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  Verifies the generated tree and the page rules. It reports structure and never judges whether a sentence is still true.
  ⚠️ A bare group letter inside backticks makes the renderer build an anchor from already-rendered HTML, producing a dead `#group-<span class=` fragment. That is `③`'s machinery and not ours to patch, so pages avoid the trigger.

### 📤 Output files · what a BUILD writes
- `../board/index.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit, and never restore the retired `board.html`.

## Law

Read Delivery first, then skill-first Engine, then Execute evidence. Design comes before all three, because it fixes what the system is and who owns its boundaries.

Delivery order is Opening, Work, Literature, Value, Display, Main, Appendix, Present, Build, Round. Venue sits inside Opening, Present includes slides and posters, Build owns diffusion and distribution, and the response unit is a Round because it is a batch.

Delivery owns content authority. Engine only routes skills across it, and Execute only records bounded runs. Tests, gates, receipts, compile checks and fresh-agent observations are all Execute evidence rather than a separate authoring layer.

A failure reopens the owning Delivery or Engine page. A failed candidate never becomes an implicit promotion.

Regrouping aligns every live page id with its current group and preserves every non-conflicting historical id as a declared alias.

## Lesson

A page count written into Content outlives two regroupings. This page carried "53 Page routes" through the growth to 63, because a number stated as a design fact is never revisited, while the same number in States is expected to move.

## Glossary

- **Delivery**: one concern or artifact a paper must author, consume, project, present, build, or revise.
- **Engine**: the reusable control model that makes paper work run consistently.
- **Execute**: a bounded real or fixture run of one Delivery through one Engine route, with inspectable evidence.
- **Round**: one external-feedback batch and its applied revision or resubmission record.

## Log

260802 · Migrated to the `QB4` page contract: Writing Style added, Content numbered into three divisions each with a face figure and caption, Aims regrouped as A1-A3 plus P with `Done when`, States mirrored one row per Aim, Files grouped by action. Two stale facts corrected in the pass: the board is 63 pages rather than 53, and `QB11`-`QB13` were added to `### 2` as series rather than being silently absent.

260801 · Consolidated 16 historical groups into QA Design, QB Delivery, QC Engine, and QF Execute; migrated page ids to their live group, retained non-conflicting aliases, and reserved QD/QE for future Paper-specific Working/Sharing content.

260801 · Aligned the Paper Board with the canonical Board-Folder and Board-Webpage contract; rebuilt 53 pages, 16 groups, and one Index; strict structure and resource checks returned zero findings.

260730 · JL replaced the proposed Test layer with Execute: Delivery says what is wanted, Engine maps skill routes, and Execute records actual bounded runs and their evidence.

260730 · Reorganized the registry Delivery first, Engine second, Execute third; added QC1 and QF1 as the two non-authoritative maps.

260730 · Reconstructed the accepted 51-page regroup after workspace recovery and recorded the implemented Build trial on QB9.

260729 · JL placed Venue inside Opening; ordered Opening → Work → Literature → Value → Display; combined diffusion/distribution with Build; kept Present for slides/posters; renamed Response to Round.

260729 · Engine plus Delivery blueprint created, preserving existing ids and requiring one overview per Delivery group.
