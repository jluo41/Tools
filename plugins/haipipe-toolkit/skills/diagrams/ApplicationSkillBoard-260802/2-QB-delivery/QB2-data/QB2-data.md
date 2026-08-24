# Delivery Data: the anchored profile the ladder stands on

state: 🔴 OPEN
owner: JL
method: state the rung's delivery and admissibility from its own skill, and route the one genuine ruling (the DIKW-Prepare pre-fill) to JL

## Opening
What does rung 1a-descriptions deliver as the D of the ladder, and what makes an entry admissible?
Rung 1a is the evidence ladder's first step: the data profile, one dated line per fact, each quoting a number a probe landed.
Interventions run on data that keeps changing, so a number with no pointer or date quietly rots under every rung built on it.
This page states what the rung delivers, the rule an entry must pass, and where a landed number may come from.

**The D of the ladder**: the family README echoes the ladder 1a to 1d against D, I, K, W, with the paper delivering K and the application delivering W.
So 1a is the application's D: the described data that everything above it interprets.

**Covered elsewhere**: which patterns emerge is 1b-themes' question, what generalizes and with what status is 1c-claims', and what the evidence advises is 1d-advice's.
The mechanics of dispatching a question and landing its answer belong to the probe layer; this page only names that lane.
QB2@paper is this page's precedent on the paper board: there the Work concern grows the discovery and task banks through explicit probes, and the task-profile probe lane feeding 1a is the application analog this page owns.

**Why it matters**: every rung above cites D ids, so one unanchored or stale entry misleads 1b, 1c, and 1d at once.
The rung's first principle says the same thing smaller: an undated anchor is a latent staleness bug.

## Writing Style
How this page must be written, so the next editor edits to the same rules.

**Quote, never compute**: any number on this page is quoted from a source the sentence names.
A sentence here that derives a new number has broken, on this very page, the first law of the rung it describes.

**Column names only**: when the subject is schema, name fields and never data values.
That is the rung's PHI rail, and it binds this page as much as it binds the artifact.

**Use the rung's vocabulary**: anchored, resolving pointer, as-of date, D id, STALE, values: lane.
A synonym invented here is a coined word the Glossary would owe a definition for, so use the source word even when it is plain.

## Diagram
**The D lane**: how a number becomes an admissible entry, and what stales it.

```text
  🌱 seed ─ [FORWARD -> CLAIMS] ─▶ 📊 1a raises ## Q-Desc-<n>
  📊 1a ─ question ─▶ 🧺 1-probes/PPNN_<topic>/ ─▶ 🧮 task-profile probe
  🧮 probe ─ values: lane ─▶ ⚓ D<n> · statistic + pointer + as-of date
  ⚓ D<n> ─ cited by ─▶ 🧩 1b themes · ⚖️ 1c claims · 🎯 1d advice
  🗄 A0-DIKW-Prepare D cells ─ pre-fill? ─▶ ⚓ D<n>    (Decision Now)
  🔁 iterate ─ new data ─▶ --refresh <Dnn> ─▶ 🏷 [STALE D<n>] on citing entries
```

## Content

### 1 · What the rung delivers
**The artifact at a glance**: the five sections of 1a-descriptions.md, and the id scheme the ladder cites.

```text
  📄 0-lifecycle/1a-descriptions/1a-descriptions.md
  ─────────────────────────────────────────────────
  🗄 Dataset       name · scope · pointer, per source
  🧭 Coverage      6 facets · cohort · arms · outcomes · window ·
                   quality · benchmark · each filled or waived
  ⚓ Descriptions  ## Description <n> · one anchored line each
  ❓ Q-consumer    ## Q-Desc-<n> · what the rung cannot answer
  🔁 Refresh Log   which D ids refreshed when · who got stamped

  🏷 id scheme     Description 3 = D3 · 1b cites T1 (D3) · 1c cites C2 (T1; D3)
```
📌 This part names the one file the rung writes, and the shape every higher rung cites into.

#### 1.1 · One Description is one dated line, and the rich detail stays where it landed
(the doc quotes what landed; distributions and field inventories live in the task result)
A Description is a topic title plus one anchored line, such as the rung skill's own example `median engagement gap 41d -> tasks/A_message_design/results/summary.csv (as-of 2026-07-08)`.
The arm-by-arm rates and field inventories behind that line stay in the task or discovery result the pointer resolves to, so there is no sidecar copy to drift.
Each entry carries a short id, so Description 3 is cited as D3, and the id is ladder-local rather than shared with PP probe numbers.

#### 1.2 · The roster grows by rounds, and saturation is earned rather than declared
(lens-rotated question storms; a dry storm plus a passed self-test says saturated)
Each round storms questions under a rotated lens: schema first, then distribution, then crossing and surprise.
A question answerable from existing D entries is discarded; the rest become D slots, each with a probe question.
The rung stops only when a storm comes up dry and a blind self-test can be answered from D entries alone, one D id per answer.

#### 1.3 · Coverage is a floor of six facets, and a waiver is banked rather than lost
(cohort, arms, outcomes, time window, data quality, benchmark)
Each facet is either filled with D ids or waived with a one-line why.
The family README's lens table makes those waived facets the rung's reservoir, re-mined at the next round's DRAFT.

### 2 · The admissibility rule
**One admissible entry**: three required parts, two exclusions, one landing lane.

```text
  ⚓ ADMISSIBLE   statistic + resolving pointer + as-of date · one line
  🚪 LANDS VIA    task-profile probe · the values: lane
  🌱 CONSUMES     seed's [FORWARD -> CLAIMS] pointers · unconsumed fails CHECK
  🚫 NEVER        computed inline · estimated in prose
  🚫 NEVER        raw rows · data values · schema sweep = column names only
```
📌 This part states the rule an entry must pass, and the one door a number may enter through.

#### 2.1 · Three parts, and the date is the part people forget
(the statistic says what, the pointer says where, the as-of date says when it was last true)
The statistic states the fact, the pointer resolves to the project-side artifact that computed it, and the as-of date says when that was last checked.
Drop the date and the entry still reads fine today, which is exactly how it misleads later.

#### 2.2 · The rung receives evidence and never produces it inline
(LAW 1: descriptions raises questions; the probe layer binds them to the bank)
DRAFT turns each question the doc cannot answer into a D slot plus a probe question, and PROBE dispatches it through haipipe-application-probe.
The values: lane lands the anchored one-liner into the Description entry; the rung never runs a computation to fill a slot, however small the computation.
Raw rows never enter either: the schema sweep reads column names only, which is the PHI rail.

#### 2.3 · Seed's forward pointers are the rung's first inputs
(this rung is the ladder's first consumer, and an unconsumed pointer fails CHECK)
DRAFT first greps seed's _LOG_0-seed.md for [FORWARD -> CLAIMS] lines and routes each data-profile need to a probe question here.
A verdict-shaped need routes onward to 1c-claims' ledger instead, so what this rung owes seed is consumption, not answers.

### 3 · Staleness and the upstream store
**The refresh chain**: iterate brings new data, 1a refreshes, and the dependents get stamped.

```text
  🔁 iterate ─▶ --refresh <Dnn> ─▶ ⚓ D<n> line + as-of date updated
  🔎 then grep 1b-themes.md · 1c-claims.md · 1d-advice.md for D<n>
  🏷 append [STALE D<n> refreshed <date>] to each citing entry
  🚦 a rung's CHECK fails on its own unresolved STALE tags

  🗄 _WorkSpace/7-AgentStore/A0-DIKW-Prepare/<DATE>_<COHORT>/
     parquet + typed D/I/K/W cells · candidate pre-fill (Decision Now)
```
📌 This part traces the dynamic-data contract this rung owns, and names the upstream store that could shortcut it.

#### 3.1 · 1a owns the stamp, and each rung clears its own
(refresh here, stamp downstream, clear locally: three owners, no ambiguity)
After any refresh this rung greps 1b-themes.md, 1c-claims.md, and 1d-advice.md for the refreshed D id and appends the STALE tag to each citing entry.
The tag clears only when that rung re-confirms or revises its own entry, and the refresh pass is recorded in this doc's Refresh Log.
This is why the artifact carries a Refresh Log even when it is empty: an intervention's data is expected to move.

#### 3.2 · The DIKW-Prepare store is a landed artifact, and whether it counts is JL's call
(typed D cells already carry computed statistics; the open question is the pointer they would anchor to)
`_WorkSpace/7-AgentStore/A0-DIKW-Prepare/<DATE>_<COHORT>/` holds parquet plus typed insight cells graded D, I, K, and W.
A typed D cell is a computed, dated statistic sitting outside the intervention, which is the same shape as a probe-landed number.
Whether its cell path counts as a resolving pointer, or whether every pre-fill must be re-landed through a task-profile probe, is the Decision Now row in States.

## Aims

### A1 · 📄 What the rung delivers
- A1.1 · A cold reader can name the artifact's five sections and say what a D id is from §1 alone.
  **Done when:** a zero-background read of §1 lists Dataset, Coverage, Descriptions, Q-consumer, and Refresh Log, and restates the D3 citation chain without opening the rung skill.

### A2 · ⚓ The admissibility rule
- A2.1 · The rule is stated as one testable line with its two exclusions.
  **Done when:** §2 gives statistic, resolving pointer, and as-of date as the three parts, and names inline computation and raw rows as the two things an entry may never contain.
- A2.2 · The probe lane is named as the only landing path for a new number.
  **Done when:** §2 names the values: lane as the door, and no sentence on this page suggests a second one until A3.2's ruling adds or refuses it.

### A3 · 🔁 Staleness and the upstream store
- A3.1 · The refresh chain is traced end to end with each owner named.
  **Done when:** §3 runs from `--refresh <Dnn>` through the [STALE D<n> refreshed <date>] stamps to the citing rung's failing CHECK, and says who clears what.
- A3.2 · The DIKW-Prepare pre-fill lane has a ruling.
  **Done when:** JL answers the Decision Now row, the ruling lands in a Law entry with the rejected option and its reason, and §3.2 states whether a typed D cell counts as anchored as-is.

## States

### Decision Now
- [ ] 🗣 May a typed D cell from the DIKW-Prepare store pre-fill a Description entry as-is?
      📍 `§3.2` the paragraph that names the store and stops short of ruling
      🔔 `Why now` the store already holds computed, dated D cells for SMS cohorts, and every one re-landed through a probe is paid for twice.
      ⭐ `A ·` the cell path counts as a resolving pointer: pre-fill directly, carry the cell's own as-of date, and refresh still runs through `--refresh` probes; CC recommends A because the rule tests the anchor rather than the courier, and a typed cell is already a landed, dated artifact.
      `B ·` pre-fill creates draft slots only: every entry must be re-landed through a task-profile probe before it counts as anchored, which keeps one evidence door at the price of recomputing what the store already computed.
      🛑 `Blocks` §3.2 stating the admissibility of pre-filled entries; until then this page treats probe-landed entries as the only anchored kind.
      🤖 `If nobody answers` B's behavior stands: entries keep landing through probes only, because a default should not widen admissibility without a ruling.

### A1 · 📄 What the rung delivers
- 🔨 A1.1 · Written into §1 from the rung skill's artifact table and round loop; no zero-background read has been run yet.

### A2 · ⚓ The admissibility rule
- 🔨 A2.1 · Written into §2.1 and §2.2 from the skill's done-criteria; nothing yet checks a live intervention's entries against it from this page.
- 🔨 A2.2 · Written into §2.2; the sentence stands, and A3.2's ruling may add a second lane or refuse one.

### A3 · 🔁 Staleness and the upstream store
- 🔨 A3.1 · Written into §3.1 from the skill's refresh contract; no live refresh pass has been traced against it.
- 🧠 A3.2 · Waiting on JL: the Decision Now row above is unanswered, so §3.2 names the store and stops short of ruling.

## Files

📥 **Input files** · what this page read

- `../../../../application/_old/1-lifecycle/1a-descriptions/haipipe-application-descriptions/SKILL.md`
  The rung contract: the anchored-entry rule, the four phases, the done-criteria, and the refresh and stamp mechanics quoted in §1 to §3.
- `../../../../application/README.md`
  The family structure: the flywheel figure, the lens and reservoir table, and the D-to-W framing the Opening leans on.
- `../../../PaperSkillBoard-260725/board.md`
  QB2@paper, the precedent: the paper's Work grows the banks through explicit probes, and this page states the application analog.

## Glossary

- ⚓ **Anchored**: carrying a statistic, a resolving pointer to the artifact that produced it, and an as-of date; the rung admits nothing less.
- 🏷 **D id**: the short name of one Description entry, so Description 3 is D3; ladder-local, cited by 1b as T1 (D3) and by 1c as C2 (T1; D3).
- 🏷 **STALE stamp**: the tag [STALE D<n> refreshed <date>] appended to a citing entry after a refresh, cleared only by that rung re-confirming or revising its entry.
- 🗄 **DIKW-Prepare store**: `_WorkSpace/7-AgentStore/A0-DIKW-Prepare/<DATE>_<COHORT>/`, the upstream store of parquet plus typed D/I/K/W insight cells named in §3.2.
- 🌱 **Pre-fill**: seeding a Description entry from an already computed upstream artifact instead of dispatching a new probe; whether it is admissible is the open Decision Now.
- 📄 **QB2@paper**: this page's precedent on the paper board, where the Work concern grows the discovery and task banks through explicit probes.

## Log

260802 · Page created against the rung skill, the family README, and QB2@paper; the DIKW-Prepare pre-fill question went to States › Decision Now instead of being ruled here.
