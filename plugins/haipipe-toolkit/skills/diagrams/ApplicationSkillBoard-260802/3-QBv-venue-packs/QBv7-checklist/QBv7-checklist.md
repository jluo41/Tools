# Checklist: the venue the reader completes
state: 🔴 OPEN
owner: JL
method: state what the pack gates, rewards, and refuses from its own two files, and record what the schema demands that the pack lacks as GAP rows instead of inventing answers

## Opening
What does the checklist venue pack know: what the channel gates, what it rewards, and what gets a draft refused?
A checklist is the one venue whose artifact the reader is meant to finish: 5 to 12 items, each with a done or not-done state, walking toward one goal.
The pack is two files, a README and a style profile, and every rule on this page is theirs.
What the schema demands and the pack does not carry is recorded as a GAP, never invented.

**Where this page sits**: one venue pack page in the QBv group, one page per channel, with the pack itself at `venue/venue-checklist/` and the pack schema one level up.

**Covered elsewhere**: the schema's other seven channels (sms, push, reminder, email, dashboard, ui-card, report) each get their own page in this group; this page owns only what is true of `venue-checklist/`.

**Why it matters**: pinning venue-checklist in an intervention's STATUS.md decides which lifecycle stages fire and how deep the claims campaign must settle before drafting, so a wrong reading of this pack either ships an unbacked item or blocks a backed one.

**What the pack cannot say**: it ships no `exemplars/` folder and no tone-by-audience rows, both demanded by `_SCHEMA.md`; §6 records both as GAPs, and §3 records the one place the pack disagrees with itself.

## Writing Style

How this page must be written; read it before editing, and edit to it.

**Inherited**: the page grammar, the section order, and the sentence rules come from the board's page contract and template and are not restated here.

**Adapted from** QBv1@paper: the desk-personality voice; the pack is spoken of as a desk with tastes, and every rule is stated as what it gates, rewards, or refuses.

**A number may be stated, but never claimed**: a count or band appears only with its source named inline (a `README.md` or `style-profile.md` section), never as this page's own claim.

**Say what the pack refuses, not what it prefers**: a preference does not decide a draft.

✅ `"Monitor glucose" is refused; "Check blood glucose before breakfast" passes`  ❌ `items should be specific`

**GAPs are recorded, never filled**: a schema-demanded answer the pack lacks becomes a GAP row in §6, and no rule on this page is invented to cover one.

## Diagram

**The pack at a glance**: what fires, how deep claims settle, the three slots, and what is refused.

```text
  🚪 GATES       seed ✓ · pitch ✓ · claims ✓ · narrative optional ·
                 display ✗ · section-edit ✗
  ⚖️ SETTLEMENT  medium · load-bearing GAP ⇒ campaign row in 1-probes/
  🧩 SLOTS       title ← pitch · items ← one K/W each · completion ← primary claim
  🔢 BUDGET      5-12 items · action verb + specific object + done state
  ❌ REFUSED     vague item · unbacked item · no done state · <5 or >12 items
  📁 ON DISK     README.md · style-profile.md · exemplars/ MISSING
```

## Content

### 1 · What the channel gates, and how deep claims must settle

**What fires at pin time**: the stages block as the README declares it.

```text
  ✅ REQUIRED   seed · claims · pitch        (the always-required spine)
  🟡 OPTIONAL   narrative                    (only when the order is an arc)
  ⛔ SKIP       display · section-edit
  ⚖️ BAR        claims_settlement: medium
```

🚪 Establishes which lifecycle stages a checklist pin fires and the bar its claims gate applies before any drafting.

The README declares three stages required, one optional, and two skipped [README.md, Stage requirements].
Seed, claims, and pitch are required at every venue in the schema, so this block's one real signal is narrative: optional here, skipped at sms, required at email [_SCHEMA.md, Stage requirements summary].
Narrative fires when the items carry a natural progression, prep to action to verify to confirm, and is skipped when the items are independent or unordered [README.md, Lifecycle mappings].
At pin time `haipipe-application-venue` translates this block into STATUS.md's `stages_skipped` row, and every downstream stage reads the pack by path [_SCHEMA.md, Stage requirements block].
The settlement bar is medium: primary claims supported or weak-with-caveat, and a load-bearing GAP must hold a campaign row, an open question in 1-probes/ [_SCHEMA.md, Claims settlement].

### 2 · The artifact: three slots, 5 to 12 completable items

**The venue template**: the fixed output structure that replaces the skipped stages.

```text
  🏷 title       names the goal               ← pitch
  ☐ items       one action, one claim each   ← one K/W per item
  🏁 completion  what success looks like      ← the primary claim

  📐 ITEM FORM   action verb + specific object + measurable completion
  ↕️ ORDER       prep → action → verify (→ confirm, when sequential)
  🔢 COUNT       5-12 · fewer too sparse · more overwhelming
```

☐ Establishes the shape a checklist draft must land in, slot by slot and item by item.

Because display and section-edit never fire, the venue template IS the artifact's structure, and the K/W-to-slot mapping happens at draft, venue-aligned, never in claims [_SCHEMA.md, Venue template].
The title slot names the goal and draws on the pitch; each item is one action backed by one claim; the completion slot says what success looks like and draws on the primary claim [README.md, Venue template].
An item is an action verb plus a specific target, with a clear done or not-done state [README.md, Constraints].
The README's own pair carries the whole format rule: "Check blood glucose before breakfast" passes and "Monitor glucose" does not [README.md, Lifecycle mappings, Draft].
Order is a logical sequence, prep to action to verify, and the rule binds only when the items are sequential at all [README.md, Constraints; style-profile.md, Drafting rules].

### 3 · What every item traces to, and where the pack's words drift

**The tracing rule and its two vocabularies**: one rule, two rungs named.

```text
  ☐ item ──▶ 📖 "one K/W entry in claims"      the pack's tracing rule
  🕳 no backing ──▶ 🚩 flag · probe when load-bearing
  📇 frontmatter     adopted_A / declined_A     the advice-rung record
  🔀 DRIFT           K/W (1c ledger) vs A (1d advice) · unruled
```

🔀 Establishes the evidence rule a checklist item must satisfy, and the one place the pack disagrees with itself.

The claims mapping is the gate: each checklist item should trace to a K/W entry, an item with no evidence backing is flagged, and a probe is opened when the gap is load-bearing [README.md, Lifecycle mappings, Claims].
The style profile repeats it as drafting rule 4: each item traces to one K/W entry in claims [style-profile.md, Drafting rules].
Its self-review then demands `adopted_A / declined_A` in frontmatter, and the A there is an advice entry: rung 1d's deliverable, the one venue-aligned stages adopt or decline [style-profile.md, Self-review checklist].
So the pack points an item at two rungs at once: the 1c claims ledger by its tracing sentence, and the 1d advice list by its frontmatter row.
Which rung an item must name changes what the draft gate checks and what gets written back into these two files, so it is JL's ruling and waits in States, under Decision Now.

### 4 · Audience and voice: two worked examples carry the whole axis

**The two voices on file**: everything the pack says about tone, it says by example.

```text
  🧑 PATIENT     "Before Your Next Visit" · plain verbs · zero ids
  🩺 CLINICIAN   "Weekly Panel Review (C3, C5)" · claim ids in the title ·
                 named surfaces ("Dashboard → At Risk")
  🔇 TONE ROWS   none · the schema expects them in this file
```

🗣 Establishes how a checklist is allowed to sound, and that the pack answers only by showing two audiences.

The schema folds audience into the pack: venue decides structure, audience decides tone, language, evidence depth, and citation format, and the style profile's tone-by-audience rows ARE the audience axis [_SCHEMA.md, Audience].
This profile carries no tone rows; it carries two worked examples, a patient pre-visit checklist and a clinician panel-review checklist [style-profile.md, Voice examples].
The clinician voice names its backing claims in the title, "(C3, C5)", and points an item at a named surface, "Review 4 high-risk refill patients (Dashboard → At Risk)"; the patient voice uses plain verbs and no apparatus at all.
A drafter writing for any audience between those two has to infer the tone from the examples, and that missing row is §6's second GAP.

### 5 · What desk-rejects a checklist

**The refusals, as the pack states them**: each is a constraint with a named cost, not a preference.

```text
  ❌ COUNT      fewer than 5 · too sparse      more than 12 · overwhelming
  ❌ ITEM       no action verb · no done or not-done state
  ❌ VAGUENESS  "Monitor glucose"               the pack's counter-example
  ❌ EVIDENCE   an unbacked item, unflagged
  ❌ ORDER      a sequential list out of prep → action → verify
```

❌ Establishes what gets a checklist draft refused, in the pack's own constraint language.

The count is a hard band, stated twice: fewer than 5 items is too sparse and more than 12 is overwhelming [README.md, Constraints; style-profile.md, Drafting rules].
An item without an action verb, or without a clear done or not-done state, fails the format constraint [README.md, Constraints].
"Monitor glucose" is the pack's own counter-example of vagueness, and the passing form names the object and the measure [README.md, Lifecycle mappings, Draft].
An item with no evidence backing is flagged at the claims gate, and a load-bearing gap opens a probe [README.md, Lifecycle mappings, Claims].
The style profile closes with a five-row self-review, and those rows are this division in checkbox form: count, verb, done state, order, frontmatter [style-profile.md, Self-review checklist].

### 6 · What the schema demands that the pack lacks

**The GAP ledger**: schema-demanded answers this pack does not carry.

```text
  📁 exemplars/           real artifacts to pattern-match · ABSENT      GAP-1
  🔇 tone-by-audience     the audience axis rows · ABSENT               GAP-2
  🔀 tracing rung         two rungs named, none ruled                   → Decision Now
```

🕳 Establishes what a reader must not expect this pack to answer, recorded rather than invented.

The schema's uniform pack layout has three parts: `README.md`, `style-profile.md`, and `exemplars/` holding real artifacts to pattern-match [_SCHEMA.md, opening block].
venue-checklist ships the first two and no `exemplars/` folder, checked on disk 260802, so a drafter imitates written voice examples with no real artifact behind them: GAP-1.
The schema says the style profile's tone-by-audience rows are the audience axis, and this profile has none: GAP-2, the missing row §4 ends on.
The K/W-versus-advice drift of §3 is not a GAP, because both answers exist in the pack; it is an unruled conflict, and it sits in Decision Now.

## Aims

### A1 · 🚪 What the channel gates, and how deep claims must settle
- A1.1 · The stages block and the medium bar are applied by the pin and the claims gate rather than recalled by a drafter.
  **Done when:** a checklist pin writes `stages_skipped` from this README and a claims CHECK run names medium as its bar.

### A2 · ☐ The artifact: three slots, 5 to 12 completable items
- A2.1 · Every checklist draft fills the three slots inside the item band.
  **Done when:** a draft names its goal, carries 5 to 12 items each in the action-verb form, and states its completion line.

### A3 · 🔀 What every item traces to, and where the pack's words drift
- A3.1 · The tracing rung is single, ruled, and written back into both pack files.
  **Done when:** `README.md` and `style-profile.md` name the same rung the ruling picked, and the draft gate checks that rung only.

### A4 · 🗣 Audience and voice: two worked examples carry the whole axis
- A4.1 · Tone-by-audience rows exist in the style profile for at least the two audiences its examples show.
  **Done when:** the profile states tone, language, and evidence depth per audience, and a drafter needs no inference from the examples.

### A5 · ❌ What desk-rejects a checklist
- A5.1 · The five-row self-review runs as a recorded draft gate, not a suggestion.
  **Done when:** a checklist draft's round records its self-review result before release.

### A6 · 🕳 What the schema demands that the pack lacks
- A6.1 · `exemplars/` exists and holds at least one real checklist artifact.
  **Done when:** `venue-checklist/exemplars/` is on disk with a real artifact and this page's Files points at it.

## States

### Decision Now
- [ ] 🗣 Which rung does a checklist item trace to: a 1c claim, the pack's K/W entry, or a 1d advice entry, the frontmatter's A?
      📍 `§3` the tracing rule and the drift it carries
      🔔 `Why now` the pack's two files point at different rungs, and neither the draft gate nor a write-back can proceed on two answers
      `A ·` keep the README's sentence: an item names one 1c claim, and adopted_A stays a separate adoption record beside it.
      ⭐ `B ·` retarget the sentence: an item names one 1d advice entry, which already derives from a 1c claim, so the item inherits its evidence through advice and the tracing rule finally agrees with the frontmatter; CC recommends B for that one-rung reason.
      🛑 `Blocks` A3.1, and any edit to the pack's two files
      🤖 `If nobody answers` nothing changes on disk, the README keeps saying K/W, and the drift stands

### A1 · 🚪 What the channel gates, and how deep claims must settle
- ⬜ A1.1 · Not started on this page's evidence; the schema names the pin as the translator and no checklist pin is cited here.

### A2 · ☐ The artifact: three slots, 5 to 12 completable items
- ⬜ A2.1 · Not started; no checklist draft stands behind this page's sources.

### A3 · 🔀 What every item traces to, and where the pack's words drift
- 🧠 A3.1 · Waiting on the Decision Now row above; no write-back before the ruling.

### A4 · 🗣 Audience and voice: two worked examples carry the whole axis
- ⬜ A4.1 · Not started; the profile carries two examples and zero tone rows, read 260802.

### A5 · ❌ What desk-rejects a checklist
- ⬜ A5.1 · Not started; the self-review block exists in the profile and nothing records a run of it.

### A6 · 🕳 What the schema demands that the pack lacks
- ⬜ A6.1 · Not started; `exemplars/` is absent on disk, checked 260802.

## Files

- `../../../../application/venue/venue-checklist/README.md`
  The hub: the constraints, the stages block, the medium bar, the three slots, and the lifecycle mappings; a rule change on this page starts here.
- `../../../../application/venue/venue-checklist/style-profile.md`
  The two audience voices, the four drafting rules, and the five-row self-review; the A3.1 write-back lands here too.
- `../../../../application/venue/_SCHEMA.md`
  What every venue pack must carry; both GAP rows in §6 are measured against it.

## Glossary

- 📖 **K/W entry**: the pack's name for one evidence entry in the claims ledger that backs one checklist item; the lifecycle's current ladder spells that territory 1c claims, with 1d advice derived from it.
- 📇 **adopted_A / declined_A**: the frontmatter record of which 1d advice entries a drafted artifact took and which it set aside; a declined entry stays available for the next round.
- 📌 **Pin**: the act of selecting one venue for an intervention, written to STATUS.md by `haipipe-application-venue`; after it, every downstream stage reads this pack by path.

## Log

260802 · Opened from `venue-checklist/`, two files read against `_SCHEMA.md`; the two schema GAPs (no exemplars/, no tone-by-audience rows) recorded in §6, and the K/W-versus-advice tracing rung put to JL in Decision Now.
