# The folder map: where a new rule, file, or page belongs

state: 🔴 OPEN
owner: JL
method: carry the map from QA1@paper across, redraw the trees from the family README and the fixture, and put the one open ruling in front of JL

## Opening
Where does a new Application rule, file, or page belong?
The one word covers three trees: `skills/application/` ships the procedure, an intervention folder such as `01_sms_young_male` holds one deliverable's story, and a project container such as `Project-Application-SMSDesign` hosts interventions beside the evidence banks.
A file in the wrong tree binds nothing, and nothing reports it.
This page draws the map and routes a new thing to its home.

**Where this page sits**: The precedent is `QA1@paper`, the same face on the paper family's board at `01-haipipe-paper-260725/QA-design/QA1-the-folder-map.md`.
That page drew the paper family's map and stated the pairing rule this page carries across; where application deliberately differs, division 3 says so and names the source.

**Why it matters**: A procedure rule written into one intervention binds that folder alone and silently drifts from the family.
Working state written into the skill tree makes the procedure wrong for every other intervention.
Neither failure reports itself, because a misplaced rule binds nothing rather than breaking something.

**Covered elsewhere**: How a stage runs its phases, how a probe binds a question to the bank, and what a venue pack holds all belong to the owning skills under `skills/application/`.
This page says only where such a file lands, never what it must contain.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4@boardform`**: the page grammar, the section order, and the sentence rules come from the board-page contract and are not restated here.

**The paper precedent is one token**: the paper family's folder-map page is cited as `QA1@paper`, never as a bare `QA1`, because this board has a QA1 of its own and the two share a title.

**Never put a count in the title or the lead**: `QA1@paper` was renamed after counts in its title went stale twice, so any number here lives in Content where a correction is an edit rather than a rename.

**A claim about the fixture carries its path**: `_fixture/` is a real folder that will change as the intervention matures, so every claim about it names the file a reader can open to see whether it still holds.

## Diagram

**The three homes**: one word, three trees, and what each one holds.

```text
 👤 /haipipe-application enter <path> · one door, three trees underneath

 🛠 THE FAMILY · skills/application/ · the procedure, shipped
    0-enter/ · 1-lifecycle/ · 2-phase/ · 3-deliver/ · 4-iterate/ · venue/

 📦 ONE INTERVENTION · 01_sms_young_male/ · one deliverable's story
    STATUS.md · 0-lifecycle/ · 0-artifacts/ · 1-probes/ · 1-rounds/ · data/

 🗂 THE CONTAINER · Project-Application-SMSDesign/ · the hosting project
    applications/ 📦📦 · tasks/ 🧱 · discoveries/ 🧱

 🧱 the banks · /haipipe-task + /haipipe-discovery own them · probe door only
```

## Content

### 1 · The family tree
**Two axes**: stages define WHAT each rung delivers, phases define HOW a rung runs.

```text
 🛠 skills/application/
    0-enter/      🚪 console · rounds
    1-lifecycle/  🎯 stage orchestrators · WHAT each stage delivers
    2-phase/      ⚙️ phase workers · DRAFT → PROBE → REVISE → CHECK
    3-deliver/    📤 artifact · review · claim-audit · deploy
    4-iterate/    🔁 post-deploy A/B refinement
    venue/        📚 venue packs · knowledge, not stages
    README.md     🧭 canonical structure · wins on layout
```
🛠 Establishes the two axes of the skill tree, and which folder a new procedure rule opens.

#### 1.1 · Stages say what, phases say how
(the two numbered groups mirror the lifecycle spine on two axes)
`1-lifecycle/` holds the user-facing stage orchestrators, one numbered folder per stage: `0-seed`, the evidence ladder `1a-descriptions` through `1d-advice`, then venue, `2-pitch`, `3-narrative`, `4-display`, and `5-section-edit`.
`2-phase/` holds the internal workers every stage drives and no user invokes: DRAFT, PROBE, REVISE, CHECK, with PROBE as the only evidence door and CHECK as the only human-involved phase.
`README.md` at the family root says of itself that it wins over anything elsewhere on layout, routing, and maturity vocabulary.

#### 1.2 · The unnumbered folders
(support groups stay flat: the router, the delivery skills, the venue packs)
`haipipe-application/` is the router and console front door, and the README names it the home of the Stage Gate Protocol.
`0-enter/` carries the console and the round verb, `3-deliver/` the artifact, review, claim-audit, and deploy skills, and `4-iterate/` the post-deploy A/B loop.
`venue/` holds venue packs, which the README calls knowledge rather than stages: a pack is consulted by the venue-aligned stages and never runs anything.

#### 1.3 · So a new procedure rule lands in the owning SKILL.md
(the placement rule for the family side, applied)
A rule about WHAT a stage delivers goes to that stage's orchestrator under `1-lifecycle/`.
A rule about HOW any rung runs its inner loop goes to the phase worker under `2-phase/`.
A layout or routing rule goes to `README.md`, the family's one canonical structure file.

### 2 · Inside one intervention
**The fixture's anatomy**: a real intervention at layer 0-seed, on this board as `_fixture/`.

```text
 📦 _fixture/ · seeded from applications/01_sms_young_male
    STATUS.md                   🧾 state header + Gate Ledger, still empty
    .intervention-console.yaml  🖥 session cache · re-derived from disk
    0-lifecycle/0-seed/         🌱 0-seed.md + _LOG_0-seed.md
    0-lifecycle/1a… 1d…         🪜 the evidence ladder · scaffolded, empty
    0-artifacts/                📤 deliverables · empty until draft
    1-probes/                   ❓ flat probe pool · empty until PROBE
    1-rounds/                   🗓 work rounds · empty until round one
```
📦 Establishes the 0-/1- split that decides where anything inside one intervention lands.

#### 2.1 · 0- is content, 1- is process
(the prefix is the placement rule, stated by the family README)
`0-` folders are the source of truth: `0-lifecycle/` is the maturation spine of stage folders each holding a `.md` plus a `_LOG`, `0-artifacts/` holds the deliverables as `<slug>-v{N}.md`, and `0-sections/` appears only for sectioned venues such as a report.
`1-` folders are process: `1-probes/` accumulates open questions as one `PPNN_<topic>/` file per topic, and `1-rounds/vYYMMDD/` holds dated work rounds.
`data/contract.yaml` joins the tree only when the pinned venue consumes data, and the fixture carries neither it nor `0-sections/` because its venue is unpinned.

#### 2.2 · What the fixture shows at 0-seed
(one deliverable's story, read off disk rather than described)
`_fixture/STATUS.md` reports layer `0-seed`, maturity `prospect`, an empty Gate Ledger, and no venue rows, because the venue stage writes those at pin time.
`_fixture/0-lifecycle/0-seed/0-seed.md` carries the five seed sections plus two Q-consumer blocks still reading `__TO_BE_FILLED__`, and its `_LOG` buffers three `[FORWARD -> CLAIMS]` pointers for rung 1a to consume.
`.intervention-console.yaml` sits outside the 0-/1- split on purpose: its own header says the console re-derives state from disk each session, so the file is cache, never truth.
Everything else exists as scaffolding only, which is what maturity `prospect` looks like on disk.

#### 2.3 · Evidence never lives here
(the banks are a wall, carried over from the paper map)
A number from the cohort or a source from the literature lands in the container's `tasks/` or `discoveries/`, owned by `/haipipe-task` and `/haipipe-discovery`.
The intervention holds only the question and the binding: a `1-probes/PPNN_<topic>/` entry binds each question by path to a QA file in the bank, and claim status lives in `0-lifecycle/1c-claims/1c-claims.md`, never in the probe file.

### 3 · The pairing rule and the deltas
**The pair and its deltas**: the family owns an artifact kind, so it earns this board.

```text
 🧩 THE THING                       📋 ITS BOARD
 🛠 skills/application/         ⟷   📌 01-haipipe-application-260802 · here

 🔑 the test (QA1@paper) · a board of one's own = the family owns a KIND
    of artifact · application owns 0-artifacts/ + the intervention shape

 ⚖️ deltas vs paper, per the README
    📄 a paper          Paper-X/ · repo-backed · submodule
    📦 an intervention  plain folder · no repo · under designs/ (§3.3)
```
🧩 Establishes why this board exists and which paper rules were deliberately not carried over.

#### 3.1 · The test, carried across
(a family earns a board when it owns a kind of artifact)
`QA1@paper` ruled that every thing has a board, and that the test for a board of one's own is whether the family owns a KIND of artifact.
Application passes it twice over: the family owns the intervention folder as a shape and the `0-artifacts/` deliverable as an artifact kind, so `01-haipipe-application-260802` is its board and holds the arguments that produce the skill tree.
The same precedent holds that a design board is a record whose rulings leave: a settled ruling graduates into the owning SKILL.md and binds from there, and division 4 routes by that rule.

#### 3.2 · Plain folders, not repos
(the delta is deliberate, and the README's deltas table is its record)
The family README states the delta in its own words: papers are repo-backed inside `Project-*` repos, interventions are plain in-project folders.
An intervention is created by the console's get-or-create with no repo backing, so placing a new one never involves a submodule.

#### 3.3 · The container, and its new home under designs/
(observed from the fixture, not yet written into the family README)
The fixture's console yaml roots the intervention at `designs/Project-Application-SMSDesign/applications/01_sms_young_male`, so the hosting container is a `Project-*` folder living under a top-level `designs/`.
`/haipipe-project` still describes `Project-*` containers as repo-backed with a submodule at `examples/<name>`, and the family README names no top-level home at all.
Whether `designs/` is the ruled home or one project's habit is a ruling that is genuinely JL's, and it waits in `### Decision Now`.

### 4 · Placing something new
**The routing table**: the page's own question, answered by what the thing IS.

```text
 📥 WHAT YOU HAVE                     📤 WHERE IT GOES
 🗣 a rule still being argued     ━▶  a Q page on this board
 ⚖️ a rule that is decided        ━▶  ## Law here → the owning SKILL.md
 🤖 a procedure an agent follows  ━▶  skills/application/ · stage or phase
 🧭 a layout or routing rule      ━▶  skills/application/README.md
 📝 one intervention's content    ━▶  its 0-lifecycle/ · 0-artifacts/
 🔄 one intervention's process    ━▶  its 1-probes/ · 1-rounds/ · STATUS.md
 🔢 a number · a source           ━▶  the banks, through the probe door
 📦 a whole new intervention      ━▶  <container>/applications/ · plain folder
```
📍 Establishes the answer a reader can apply without the rest of the page, one row per kind of thing.

#### 4.1 · The table is not yet portable
(a fresh agent should place a file from the family README alone)
`skills/application/README.md` routes verbs to skills and draws both trees, but it never answers where a new rule, file, or page lands.
Until it carries this table, the routing exists only here, which is the gap `A4.1` names.
One row is also deliberately incomplete: a new intervention's full path reads `<container>/applications/` until JL rules where a new container itself lands.

## Aims

### A1 · 🛠 The family tree
- A1.1 · The family map matches the canonical README and resolves on disk.
  **Done when:** every folder named in division 1 exists under `skills/application/`, and the map contradicts nothing in `README.md`'s Skill-tree layout section.

### A2 · 📦 Inside one intervention
- A2.1 · The 0-/1- split sorts everything inside an intervention without a third category.
  **Done when:** every top-level entry of `_fixture/` is placed as content, process, or named cache, and a reader can sort a new file by prefix alone.

### A3 · 🧩 The pairing rule and the deltas
- A3.1 · The artifact-kind test sorts the application family the way it sorted the six paper pairs.
  **Done when:** the test names the artifact kind application owns, and this board's existence is justified by it without appeal to history.
- A3.2 · The home of an application container is ruled, not inherited from one project's habit.
  **Done when:** JL answers the `designs/` row in `### Decision Now`, and the ruling is recorded with the date here and in the family README.

### A4 · 📍 Placing something new
- A4.1 · A fresh agent can place a new file from the family README alone.
  **Done when:** `skills/application/README.md` carries the routing table, and a cold agent given one new file names its folder correctly without opening this board.

### P · 🏁 Page-level
- P1 · This page obeys the page contract.
  **Done when:** `check.py` reports no finding against this page after the board's batch build.

## States

### Decision Now

- [ ] 🗣 Is `designs/` the ruled top-level home for application project containers?
      📍 `Part 3.3` the container's home, beside the plain-folder delta it belongs with
      🔔 `Why now` the fixture roots its intervention at `designs/Project-Application-SMSDesign` while `/haipipe-project` scaffolds `Project-*` containers under `examples/`, and nothing says which one binds
      ⭐ `A ·` ratify `designs/` and write it into the family README; recommended because it matches what is already on disk and costs no migration
      `B ·` fold application containers back under `examples/` beside every other `Project-*`, which buys one convention at the price of migrating the SMSDesign project
      🛑 `Blocks` nothing today; the fixture keeps working either way, and only the routing table's last row stays a placeholder
      🤖 `If nobody answers` A stands, because it is the disk state and undoing it later is one migration either way

### A1 · 🛠 The family tree
- 🔨 A1.1 · The map is drawn from `README.md` as read on 260802; each folder's presence on disk has not been checked yet.

### A2 · 📦 Inside one intervention
- 🔨 A2.1 · The fixture's top level sorts cleanly today, with the console yaml named as cache; the sort has not been tried against a venue-pinned intervention carrying `0-sections/` and `data/contract.yaml`.

### A3 · 🧩 The pairing rule and the deltas
- ✅ A3.1 · The test sorts application without amendment: the family owns the intervention folder and the `0-artifacts/` deliverable, both stated in `README.md`'s intervention layout.
- 🧠 A3.2 · Waiting on JL; the row is first in `### Decision Now`.

### A4 · 📍 Placing something new
- ⬜ A4.1 · `README.md` routes verbs to skills and draws both trees, but carries no placement table; the routing exists only on this page.

### P · 🏁 Page-level
- ⬜ P1 · The board's batch build and check have not run against this page yet.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `../../application/README.md`
  The family's canonical structure file, and the target of `A4.1`: the routing table graduates here so a cold agent never needs this board.

### 📥 Input files · what this page READS
- `../01-haipipe-paper-260725/QA-design/QA1-the-folder-map.md`
  The precedent `QA1@paper`; division 3 carries its pairing rule across and names the deltas.
- `_fixture/STATUS.md` · `_fixture/.intervention-console.yaml` · `_fixture/0-lifecycle/0-seed/0-seed.md` · `_fixture/0-lifecycle/0-seed/_LOG_0-seed.md`
  The real intervention behind division 2; open them to see what maturity `prospect` looks like on disk.

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  Owns `dead-file-path` and the section findings this page is measured by; it reads structure and never judges whether a claim about the fixture is still true.

### 📤 Output files · what a BUILD writes
- `board/QA/QA1-the-folder-map.html`
  Generated by the board build on the caller's batch run. Never hand-edit.

## Glossary

- 📦 **Intervention**: one deliverable's folder, such as an SMS campaign for one audience; the application family's unit of work.
- 🪜 **The ladder**: the venue-free evidence rungs `1a-descriptions` through `1d-advice` inside `0-lifecycle/`, which the family README draws as a flywheel rather than a one-way climb.
- 🧱 **The banks**: `tasks/` and `discoveries/` in the hosting container, owned by their own skills and reached from an intervention only through the probe door.
- 📌 **Venue**: the output modality (sms, email, dashboard, report), pinned after the ladder; it gates stages 3 to 5 and sets how deeply claims must settle.
- 🔗 **Pairing rule**: every thing has a board, and a family earns a board of its own when it owns a kind of artifact; stated and argued on `QA1@paper`.

## Log

260802 · Page created on the board's opening batch: the three trees mapped from the family README, the fixture read at maturity `prospect`, the pairing rule carried from `QA1@paper`, and the `designs/` home raised to JL in `### Decision Now` rather than assumed.
