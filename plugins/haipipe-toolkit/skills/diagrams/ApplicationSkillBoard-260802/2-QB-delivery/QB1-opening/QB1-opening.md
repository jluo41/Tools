# Brief: why the intervention exists, where it ships, and what it promises
state: 🟡 PARTIAL
owner: JL
method: bind the seed wager, the venue pin, and the pitch into one reader-facing concern, mirroring QB1@paper without copying its paper-only stage order
session: 238a70b8-04b7-4c27-ad56-7c1932584c06

## Opening
What does a reader get in an Application Brief, and where does each part live?

**Naming ruling (260817)**: Application's formal Page Type is `Brief`, not `Opening`. Paper keeps the globally unique `Opening` type. This folder retains the historical board id `QB1-opening` so old links remain readable; its Seed + Venue + Pitch material migrates into one Brief Page.

The seed says why it might work, the pin says which channel ships it, and the pitch says what it promises there.
Each is settled at a different moment, with the whole evidence ladder between the first two, so the three drift into three folders.
This page binds them into one concern and names the file home of each answer.

**Where this page sits**: it is the first Delivery concern on this board.
The evidence ladder, rungs 1a-descriptions through 1d-advice, settles what is true and belongs to its own concern; this page records only that the pin waits on the ladder's 1d gate.
The stages after pitch (narrative, display, section-edit) are venue-ALIGNED work downstream of this concern and are not written here.

**The mirrored ruling**: on the paper board, QB1@paper ruled that the venue DECISION lives inside Opening while the venue CATALOG is its own group.
This page adopts the same split: the pin and its downstream contract live here, and the per-venue packs under `venue/venue-<name>/` stay knowledge that no page restates.

**Covered elsewhere**: what the evidence actually shows belongs to the ladder's pages, and how a raised question binds to the bank belongs to the probe layer.
This page owns the three answers, their file homes, and what refutes each.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Say the three in reader order**: the order carries the argument for the grouping.

✅ `seed, venue pin, pitch`  ❌ `seed, pitch, and also the venue`

Any other order makes the pin look appended, which is the reading QB1@paper's ruling overturned.

**Never restate a venue pack**: the packs are knowledge, not decisions.
This page states the pin, its three STATUS rows, and the contract file, and stops.

**Keep the ladder out**: a sentence about what the evidence shows belongs on the ladder's own pages.
A sentence about whether an Opening answer is settled belongs here.

**Cite the paper precedent as the plain token QB1@paper**: a bare QB1 on this board is this page, so the token is what keeps a figure from linking the wrong board.

**Language and sentences**: English only, one sentence per line, plain words for a weak-English reader, no em-dashes.

## Diagram
**The Opening contract**: three answers, the file home of each, and the gate between them.

```text
   🌱 SEED WAGER            📌 VENUE PIN               📣 PITCH
   why it might work        where it ships             what it promises
        │                        │                          │
        ▼                        ▼                          ▼
   📄 0-lifecycle/          📋 STATUS.md · 3 rows      📄 0-lifecycle/
      0-seed/0-seed.md      📄 0-lifecycle/               2-pitch/2-pitch.md
                               2-venue/2-venue.md
        │                        ▲                          ▲
        └─🪜 1a ▸ 1b ▸ 1c ▸ 1d ──┘ 🚪 1d gate     🔁 re-pin ─┘

   🧷 venue-FREE      seed · the ladder
   🧵 venue-ALIGNED   pitch and every stage after it
   🚫 not here        ladder evidence · venue-pack knowledge
```

## Content

### 1 · One legacy opening concern, one Brief Page
**Promise and refuter, per answer**: what downstream reads, and what knocks each answer down.

```text
   answer     📤 promises downstream             💥 refuted by
   ────────────────────────────────────────────────────────────
   🌱 seed    the why · audience · mechanism     👣 occupied ground
   📌 pin     3 STATUS rows · the principles     📉 settlement gap
   📣 pitch   goal · [primary] · the chain       🔗 unanchored link
   ❓ open    wager vs ladder evidence           🗳 Decision Now row
```
🧾 This part states what the three answers promise the stages after them, and the concrete thing that knocks each one down.

#### 1.1 · What the Brief promises downstream
(after the pin, every stage reads two files, and this page says which two)
After the pin, any stage can name its channel contract, its skipped stages, and its settlement bar from two files: the three rows in `STATUS.md` and the Artifact Principles in `2-venue.md`.
The pitch sells only what the ladder settled, so a downstream reader never meets an unanchored promise.
The seed's why survives every retarget, so the intervention's reason for existing stays stable however often the channel changes.

#### 1.2 · What refutes each answer
(one concrete refuter per answer, and the one whose consequence is not ruled)
The seed is refuted by its own feasibility probes: the angle turns out to be occupied ground, or the external design base cannot be obtained.
The pin is refuted by the Fit Assessment in `2-venue.md`: a venue whose settlement bar sits above what the Evidence Campaign has settled must wait for more settlement or be swapped for a lighter venue.
The pitch fails its own definition of done when a theory-of-change link cites no advice entry (`A<n>`) and no supported claim (`C<n>`), and a re-pin rewrites it whole.
The fourth refuter is the ladder itself contradicting the wager, and none of the three stage contracts read here rules its consequence, so it sits in Decision Now below.

#### 1.3 · The ladder sits inside this concern's span, on purpose
(seed is stage 0, pin and pitch come after rung 1d, and the hole is the price of reader order)
The lifecycle runs seed, then rungs 1a to 1d, then venue, then pitch, so this concern holds the two ends while the ladder fills the middle.
Grouping by what a reader asks rather than by when the machine runs is the same trade QB1@paper recorded, and pinning AFTER the 1d gate is what keeps the ladder venue-FREE all the way up.

### 2 · The seed wager
**The seed's shape**: five statements and a bounded probe budget, all venue-FREE.

```text
   📄 0-lifecycle/0-seed/0-seed.md            🧷 venue-FREE
   ──────────────────────────────────────────────────────────
   💡 Opportunity        the gap · the behavior to move
   📈 Expected impact    2-5pp young-male engagement lift
   👥 Audience           young men 18-35 in SMSR2Full
   📡 Channel hunch      sms · a hunch, never the pin
   🧠 Mechanism          direct, autonomy-supportive framing
   ❓ Q-consumer         Q-Seed-1 novelty · Q-Seed-2 obtainable

   📤 [FORWARD -> CLAIMS]   internal-data needs · 3 in the log
```
🌱 This part states what the seed commits to before any evidence exists, and where its questions are allowed to go.

#### 2.1 · Five statements made before evidence is mature
(the wager: opportunity, impact, audience, channel hunch, mechanism)
The seed answers one question, why might this intervention work, in five sections: Opportunity, Expected impact, Audience, Channel hunch, and Mechanism hypothesis.
The fixture's wager is concrete: young men aged roughly 18 to 35 in the SMSR2Full cohort are the documented low-response segment, and picking the best framing arm for them should lift SMS engagement 2 to 5pp over the generic arm.
Everything above it on the ladder grows from this file, and it is written before rung 1a has profiled a single patient.

#### 2.2 · The channel hunch is context, never the pin
(sms in the fixture, and the seed survives a retarget untouched)
The fixture names sms as its hunch because SMSR2Full is itself an SMS field study, and the hunch commits nothing.
The pin happens after the ladder, in different files, so a retarget rewrites the pitch and leaves `0-seed.md` unedited.

#### 2.3 · Feasibility is the seed's whole probe budget
(two probe shapes go out, and internal-data needs leave as pointers)
The seed may probe two shapes only, both discovery-side: is the angle novel, and is the external design data obtainable; the fixture raises exactly these as Q-Seed-1 and Q-Seed-2.
Profiling our own cohort is rung-1a task work, so it leaves as a `[FORWARD -> CLAIMS]` pointer in `_LOG_0-seed.md`, and the fixture log carries three.
The pointer token stays `CLAIMS` even though rung 1a consumes it, because the consuming grep is frozen on that word and a reworded token silently disappears.

### 3 · The venue pin
**The pin's writes**: three STATUS rows and one contract file, written after the 1d gate.

```text
   🚪 runs AFTER the 1d gate · BEFORE pitch
   ──────────────────────────────────────────────────────────
   📋 STATUS.md     | venue             | sms                |
                    | stages_skipped    | narrative display… |
                    | claims_settlement | light              |
   📄 2-venue.md    🧩 Artifact Principles · channel-HOW
                    ⚖️ Fit Assessment · the settlement delta

   👀 row readers   strip · router · claims gate · composer
   🔁 retarget      re-runs venue · the ladder SURVIVES
```
📌 This part states what pinning writes, who reads it, and which half of the downstream contract it owns.

#### 3.1 · Three STATUS rows the whole system reads
(venue, stages_skipped, claims_settlement, and their four readers)
The pin writes three rows into `STATUS.md`: `venue`, `stages_skipped`, and `claims_settlement`.
The stage strip, the lifecycle router, the claims gate, and the artifact composer all read them, which is why they live in the state file rather than inside the venue page.
An sms pin skips narrative, display, and section-edit and sets a light settlement bar; a dashboard or report pin skips nothing and demands full settlement.
On the fixture the rows are absent, because the venue is not yet pinned and `STATUS.md` says so in as many words.

#### 3.2 · Artifact Principles is channel-HOW, and 1d advice is content-WHAT
(two contracts with two owners, and downstream stages read the shape here)
`2-venue.md` distills the venue pack and the audience profile into concrete specs: template and slots, length limits, tone by audience, element types, settlement and gate depth, compliance rails.
That is channel-HOW, how to shape the deliverable, and it is a different contract from 1d-advice's content-WHAT, what the evidence advises the message to say.
Pitch, display, section-edit, and artifact read the shape here instead of re-deriving it from the pack per stage.

#### 3.3 · A re-pin rewrites downstream and spares the ladder
(the decision gate is re-runnable, and the evidence is what survives it)
Changing venue re-runs this stage: `2-venue.md` rewrites with new Artifact Principles, and pitch, narrative, display, and section-edit rewrite with it.
The claims ledger survives; a heavier venue raises `claims_settlement`, which is more settlement work on the same campaign rather than invalidation.
The seed is spared for the same reason the ladder is: why the intervention exists does not change with the channel, only what it promises there does (JL 260802, mirrored from QB1@paper; see `## Law`).

### 4 · The pitch
**The pitch's shape**: the one-minute story, every link anchored, one claim designated.

```text
   📄 0-lifecycle/2-pitch/2-pitch.md         🧵 venue-ALIGNED
   ──────────────────────────────────────────────────────────
   🎯 One-sentence goal   specific + testable
   ⛓ Theory of change    each link ━▶ A<n> or C<n>
   👥 Audience frame      register + the ask
   🏅 Primary claim       [primary] · lives HERE, not the ledger
   ⏰ Why now             what makes it timely

   🚧 no pin in STATUS.md   ━▶ BLOCK · run venue first
   🔁 re-pin                ━▶ the pitch rewrites whole
```
📣 This part states what the pitch owes the pinned venue's reader, and why it is the first casualty of a retarget.

#### 4.1 · First venue-ALIGNED stage, and blocked without a pin
(it reads the pin's contract, never the raw packs)
The pitch reads the pinned `2-venue.md` Artifact Principles and the audience profile, not the venue packs.
A `STATUS.md` with no venue row blocks it outright, so a pitch can never quietly precede its own channel.

#### 4.2 · One minute, every link anchored
(the theory of change receives evidence and never produces it)
The pitch is the one-minute story of what the intervention achieves and why it should work.
Its theory of change is a causal chain from message to behavior, and every link cites a 1d advice entry (`A<n>`) or a supported ledger claim (`C<n>`); an unanchored link fails the stage's own definition of done.
Evidence is received here, never produced: the ladder settled it upstream, and a beat exposing a new gap routes back to the claims ledger instead of gathering here.

#### 4.3 · The [primary] designation lives here, venue-aligned
(the ledger ranks nothing, and the pitch names the one claim that sells)
The venue-free ledger holds claims without ranking them, and the pitch names the ONE that carries the value proposition for this venue and audience.
A result novel elsewhere but already assumed by this audience is an enabler, not the primary.
The designation re-runs on every re-pin, which is why it lives in the pitch and not in the ledger.

## Aims

### A1 · 🧾 One legacy opening concern, one Brief Page
- A1.1 · Every downstream stage can find the three answers from this page alone.
  **Done when:** each answer names its exact artifact path here, and all three paths resolve on a pinned intervention without editing this page.
- A1.2 · Each answer's refuter is stated beside its promise.
  **Done when:** `§1.2` names one concrete refutation per answer, and the unruled one carries a Decision Now row instead of a guess.

### A2 · 🌱 The seed wager
- A2.1 · The seed's venue freedom is preserved in this page's own wording.
  **Done when:** this page never treats the fixture's sms hunch as a pin, and a re-pin leaves `0-seed.md` unedited.
- A2.2 · The seed's probe budget is bounded to feasibility.
  **Done when:** `§2.3` names the two probe shapes and the `[FORWARD -> CLAIMS]` pointer, and no ladder evidence work is described as the seed's.

### A3 · 📌 The venue pin
- A3.1 · The pin's three STATUS rows and their readers are stated.
  **Done when:** `§3.1` lists `venue`, `stages_skipped`, and `claims_settlement` and names the consumers that read them.
- A3.2 · Channel-HOW stays distinct from content-WHAT.
  **Done when:** Artifact Principles and 1d advice appear as two contracts with two owners, and no advice content is restated on this page.

### A4 · 📣 The pitch
- A4.1 · The [primary] designation is placed on the pitch, not the ledger.
  **Done when:** `§4.3` states the designation's home and that a re-pin re-runs it.
- A4.2 · The anchor rule is stated as the pitch's own done-check.
  **Done when:** `§4.2` states that every theory-of-change link cites an `A<n>` or `C<n>`, matching the pitch skill's definition of done.

### P · 🏁 Page-level
- P1 · Refutation of the wager by the ladder has a ruled consequence.
  **Done when:** JL answers the Decision Now row and the ruling lands in `## Law` with the rejected option and the date.

## States

### Decision Now
- [ ] 🗣 If the ladder shows the seed's wager is wrong, what closes: the seed or the intervention?
      📍 `Part` §1.2, beside the three refuters whose consequences are already ruled
      🔔 `Why now` the fixture's rung 1a will profile young-male engagement, and a flat profile contradicts the Opportunity's premise
      ⭐ `A ·` amend the seed in place and re-run the ladder: the folder stays alive, the old wager stays in `_LOG_0-seed.md`, and every rung re-gates; CC recommends A because it is reversible, and closing stays available if the amended wager also fails
      `B ·` close the intervention and keep the refuted seed as its record: a new wager gets a new folder, so no seed file ever says two different whys
      🛑 `Blocks` nothing today; the fixture has not run rung 1a
      🤖 `If nobody answers` A takes effect

### A1 · 🧾 One legacy opening concern, one Brief Page
- 🔨 A1.1 · Written into `§1.1` and the Diagram; the fixture holds only `0-seed.md` today, so two of the three homes cannot be opened yet.
- 🔨 A1.2 · `§1.2` names a refuter per answer; the wager's own refutation waits on the Decision Now row above.

### A2 · 🌱 The seed wager
- 🔨 A2.1 · Stated in `§2.2` from the seed skill's own rule and now ruled in `## Law` rather than only derived; no re-pin has happened on the fixture, so survival is untested.
- ✅ A2.2 · `§2.3` names both probe shapes and the pointer; the fixture's `_LOG_0-seed.md` carries three `[FORWARD -> CLAIMS]` pointers and no internal-data probe, read 260802.

### A3 · 📌 The venue pin
- 🔨 A3.1 · Stated in `§3.1` from the venue skill; the fixture's `STATUS.md` confirms the rows are absent until pin time, so no live example of the three rows exists on this board yet.
- 🔨 A3.2 · The two-contract split is stated in `§3.2`; no reviewer has checked this page for leaked advice content.

### A4 · 📣 The pitch
- 🔨 A4.1 · Stated in `§4.3`; the fixture has no `2-pitch/` folder yet, so the designation has no live example to check against.
- 🔨 A4.2 · Stated in `§4.2` from the pitch skill's definition of done.

### P · 🏁 Page-level
- 🧠 P1 · Waiting on JL; the Decision Now row above carries the options and the default.

## Files

📋 **Contracts** · what carries a rule between this page and another

- `../../../PaperSkillBoard-260725/board.md` · the paper precedent, cited in prose as QB1@paper; it holds the ruling this page mirrors, that the venue decision is Opening's and the venue catalog is not

📥 **Input files** · what this page reads and restates

- `../../../../application/_old/1-lifecycle/0-seed/haipipe-application-seed/SKILL.md` · the seed contract `§2` restates: five sections, feasibility-only probes, forward pointers
- `../../../../application/_old/1-lifecycle/haipipe-application-venue/SKILL.md` · the venue contract `§3` restates: three STATUS rows, Artifact Principles, retarget semantics
- `../../../../application/_old/1-lifecycle/2-pitch/haipipe-application-pitch/SKILL.md` · the pitch contract `§4` restates: anchored theory of change, the [primary] designation
- `_fixture/0-lifecycle/0-seed/0-seed.md` · the worked seed every example on this page comes from
- `_fixture/0-lifecycle/0-seed/_LOG_0-seed.md` · the fixture's phase journal and its three `[FORWARD -> CLAIMS]` pointers
- `_fixture/STATUS.md` · where the pin's three rows will land on the fixture; today it states the venue is unpinned

## Law

- 260817 JL · ⚖️ The formal Application Page Type is Brief. `Opening` is reserved for Paper; legacy Seed + Venue + Pitch fold into Brief.

- 260729 JL · ⚖️ The venue decision is Opening's, and the venue catalog is not
      The pin and its downstream contract live on this page; per-venue pack knowledge takes its own group and no page restates it.
      Ruled on the paper board (QB1@paper) on 260729 and sharpened in that board's QBv group note on 260802 when the catalog group opened; mirrored onto this board by the 260802 assignment. Rejected: a separate venue concern, because it made the work read as though it chose a channel after deciding what it argued.
- 260802 JL · ⚖️ A re-pin reopens the pitch and leaves the seed
      Why the intervention exists does not change with the channel; what it promises there is shaped by one, so `2-venue.md` and every venue-ALIGNED stage from pitch onward rewrite whole while `0-seed.md` is left unedited and the ladder's evidence survives.
      Ruled on the paper board (QB1@paper) on 260802, when JL answered its Decision Now with A; mirrored onto this board because `§2.2`, `§3.3`, and `A2.1`'s done-when all rest on it. Rejected: re-gating the whole concern on every retarget, because that reopens a seed nobody intended to change; and reopening nothing automatically, because two interventions retargeted the same way would then end in different states.

## Glossary

- 🌱 **Wager**: the seed's five venue-free statements (opportunity, expected impact, audience, channel hunch, mechanism hypothesis), made before rung 1a has touched the data.
- 📌 **Pin**: the venue stage's write of the `venue`, `stages_skipped`, and `claims_settlement` rows into `STATUS.md`, after which every downstream stage couples to the channel.
- 🪜 **Ladder**: the venue-FREE evidence rungs, 1a-descriptions to 1d-advice, that run between the seed and the pin.
- 🧩 **Channel-HOW / content-WHAT**: the split the venue contract draws: `2-venue.md`'s Artifact Principles say how to shape the deliverable, and 1d-advice says what the evidence advises it to say.
- 🔗 **QB1@paper**: the paper board's Delivery Opening page, written as a plain token so it never links as this board's own QB1.

## Log
260817 · Renamed the formal Page Type to Brief, preserved `QB1-opening` as a legacy board id, and mapped Seed/Venue/Pitch into the Brief contract.
260802 · Page created from the assignment packet: seed, pin, and pitch bound as one Opening concern mirroring QB1@paper, and the wager-refutation fork opened in Decision Now.
260802 · The retarget rule, a re-pin reopens the pitch and leaves the seed, mirrored from QB1@paper into `## Law` with its rejected options; `§3.3` anchored to it and A2.1's State updated, because `A2.1`'s done-when rested on a ruling this board had not recorded. Provenance of the 260729 entry corrected to the paper board's QBv group note, and `§1.2`'s pin refuter reworded from refused to refuted.
