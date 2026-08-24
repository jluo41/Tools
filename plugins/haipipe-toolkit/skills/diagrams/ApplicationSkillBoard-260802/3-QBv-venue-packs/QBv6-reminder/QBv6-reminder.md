# Reminder: the venue whose message is a time

state: 🔴 OPEN
owner: JL
method: state what the pack gates, rewards, and refuses, and record the scheduling it does not record as GAP items for JL to close

## Opening

A reminder is the venue whose message is a time: the text is at most 200 characters, and the decision that matters is when it fires and how often it returns.
So what does this pack actually know about what the channel gates, rewards, and requires?
Its two files answer the text half well and the time half not at all.
This page states what the pack knows and records the missing half as GAP items instead of inventing it.

**Where this page sits**: one venue pack per page in `QBv`; the sibling `QBv` pages own the other venue packs `_SCHEMA.md` lists (sms, push, checklist, email, dashboard, ui-card, report), and this page owns only `application/venue/venue-reminder/`.

**Why it matters**: when `haipipe-application-venue` pins reminder, every downstream stage reads this pack and nothing else, so a pack that records no scheduling means the draft stage improvises the one thing this channel is for.

**Shape precedent**: the desk-personality voice is adapted from QBv1@paper, which reads a venue as a desk with tastes; here the desk is a scheduler, so the tastes are about time.

**What is thin**: the pack is two files totalling 96 lines (58 + 38, measured 260802), has no `exemplars/`, and records no anchor events, offsets, or escalation.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited**: the page grammar, the section order, and the sentence rules come from `haipipe-board/ref/page-template.md` and are not restated here.

**A number is stated with its source**: a character budget or variant count carries the pack line that records it, and a measurement this page made carries its date.

**Say what the channel refuses, not what it prefers**: a preference does not stop a design.

✅ `a single static reminder is refused`  ❌ `variety is encouraged`

**A GAP is recorded, never filled**: where the schema or the channel demands an answer the pack lacks, this page writes the GAP and stops; the value arrives from the pack or from a JL ruling, never from this page.

## Diagram

**The reminder venue at a glance**: what fires, what the artifact is, and where the pack goes silent.

```text
  ⏰ CHANNEL    time-triggered · recurring · ≤ 200 chars ·
                daily / weekly / event-triggered

  🚪 GATES      seed ✓ · claims ✓ · pitch ✓
                narrative ✗ · display ✗ · section-edit ✗ · bar LIGHT

  🧩 TEMPLATE   prompt ~100 · motivation ~80 · encouragement ~20
                3-5 variants rotate · motivation is the moving part

  ❌ REFUSED    > 200 chars · nagging · one static message ·
                no question hook

  🕳 SILENT ON  anchor event · offset · escalation · stop rule ·
                exemplars/ · tone by audience
```

## Content

### 1 · What the channel gates: three stages fire, three skip

**The gate row and the bar**: which lifecycle stages fire under this venue, and how deep claims must settle.

```text
  🚪 FIRE       seed · claims · pitch
  🚫 SKIP       narrative · display · section-edit
  🧩 IN PLACE   the 3-slot venue template, filled at draft
  ⚖️ BAR        light · named K/W or common knowledge ·
                non-load-bearing GAPs allowed
```

🚪 Establishes reminder as a minimum-lifecycle venue: the three always-required stages fire, nothing else does, and a fixed template stands where the skipped stages would.

#### 1.1 · Only the minimum lifecycle fires
(seed, claims, and pitch are required at every venue; this venue adds nothing to them)
`_SCHEMA.md` makes seed, claims, and pitch always required, the minimum viable lifecycle.
The reminder README's stages block marks narrative, display, and section-edit as skip, so this venue runs exactly that minimum [README, stage requirements].
At pin time `haipipe-application-venue` translates the block into the STATUS.md `stages_skipped` row [_SCHEMA.md, stage requirements block].
The venue template replaces the skipped stages with a fixed output structure, and the K/W-to-slot mapping happens at draft, venue-aligned, never in claims [_SCHEMA.md, venue template].

#### 1.2 · Light is the lowest settlement bar
(what the claims CHECK gate asks before any artifact work)
`claims_settlement: light` asks that every claim the artifact leans on be tied to a named K/W or to common knowledge, and it lets a GAP pass when it is not load-bearing [_SCHEMA.md, claims settlement].
The pack's own claims mapping sizes the ledger at 1-2 K/W entries, with the motivation slot cycling through different framings across instances [README, lifecycle mappings].
So the evidence work this venue demands is small on purpose: the channel bets on repetition, not on argument.

### 2 · What the channel rewards: a rotating set, never one message

**One reminder, three slots**: the fixed shape of an instance and the moving part of the set.

```text
  📣 PROMPT         ~100 chars · names the action · action claim (W)
  💡 MOTIVATION     ~80 chars · the reason why · primary claim (K) ·
                    the only slot that varies
  🌤 ENCOURAGEMENT  ~20 chars · positive close · standard
  🔁 THE SET        3-5 variants rotate · ≤ 200 chars each ·
                    one question hook per variant
```

🔁 Establishes the deliverable as a set of 3 to 5 rotating variants whose only moving part is the motivation slot.

#### 2.1 · Repetition is the mechanism, fatigue is its price
(why the venue rewards a set instead of one good message)
The README names the bet in its first line: brief, predictable, builds habit through repetition.
The same repetition is the failure route, so the constraints demand slight variation across instances to avoid fatigue [README, constraints].
The drafting rules make that concrete: 3 to 5 variants rotate, the motivation slot varies, and the prompt and encouragement slots hold still [style-profile, rules 1 and 3].
The three voice examples show it: the ask stays a check-in while the reason rotates from spotting patterns to staying consistent to plain encouragement [style-profile, voice examples].

#### 2.2 · Each slot has a claim source, so the ledger feeds the message
(the template is a K/W-to-slot mapping, not a copywriting form)
The prompt names the action to take and draws on an action claim at the W rung, at about 100 characters [README, venue template].
The motivation gives the brief reason why and draws on a primary claim at the K rung, at about 80 characters, varying per instance [README, venue template].
The encouragement closes on about 20 characters of standard positive reinforcement [README, venue template].
Every variant additionally carries one question as its engagement hook [style-profile, rule 5].

### 3 · What desk-rejects a reminder design

**The refusals**: each is a named line in the pack, not a taste.

```text
  ❌ LENGTH      over 200 characters          [README · Length]
  ❌ TONE        nagging                      [README Tone · style rule 4]
  ❌ VARIETY     one static message           [README Variation · rule 1]
  ❌ HOOK        no question in the variant   [style rule 5]
  ❌ RECORD      no adopted_A / declined_A    [checklist row 5]
```

❌ Establishes what a reminder design is refused for, and names the one refusal the pack's own checklist forgets.

#### 3.1 · Supportive, not nagging, is the line between a reminder and spam
(the tone rule appears in both files because it is the channel's survival condition)
The README's tone constraint and the style-profile's rule 4 state the same refusal in the same words: supportive, not nagging.
A recurring message that reads as nagging teaches the recipient to ignore the channel, and that spends the repetition the venue's mechanism depends on.

#### 3.2 · The checklist drops one of its own rules
(four of the five drafting rules are checked; the question hook is not)
The self-review checklist covers the variant count, the length, the motivation variation, the tone, and the advice frontmatter [style-profile, checklist].
Drafting rule 5, one question per reminder, has no checklist row, so the hook is the one refusal a draft can miss while passing its own review.
The `adopted_A / declined_A` frontmatter row is the draft's record of which design-advice entries it took and which it refused.

### 4 · What the pack does not know: the schedule is the intervention

**The GAP roster**: what the schema or the channel demands and the pack does not record.

```text
  🕳 SCHEDULING   anchor event · offset · escalation · stop rule
                  ── the pack's whole answer is one frequency row
  🕳 EXEMPLARS    exemplars/ demanded by _SCHEMA.md · absent on disk
  🕳 AUDIENCE     tone-by-audience rows · style-profile.md has none
```

🕳 Establishes the pack's blind side: the WHEN half of the channel, which is the half the venue is named for.

#### 4.1 · The scheduling logic is the intervention, and the pack has one line on it
(the frequency row lists trigger kinds; it is not a schedule)
A reminder's content is thin by design, three slots inside 200 characters, so the intervention lives in the scheduling: what event anchors the series, what offset separates the anchor from the first fire, whether an ignored instance escalates, and when the series stops.
The pack's whole answer is one frequency row: recurring, as daily, weekly, or event-triggered [README, constraints].
It never names an anchor event, an offset, an escalation policy, or a stop rule, so each scheduling row in the roster above is a GAP, recorded here and answered nowhere in the pack.
This page does not invent the answers, because each one is a design ruling rather than a fact on disk, and the ruling is JL's: the Decision Now row in States carries it.

#### 4.2 · Two parts the schema demands are missing from the folder
(measured against `_SCHEMA.md` on disk, 260802)
The schema gives every venue pack three parts: `README.md`, `style-profile.md`, and `exemplars/` holding real artifacts to pattern-match.
The venue-reminder folder holds the first two and no `exemplars/` (checked 260802).
The schema also folds the audience axis into the pack, stating that the style-profile's tone-by-audience rows ARE the audience axis, and this style-profile carries voice examples but no tone-by-audience rows.
So a reminder aimed at a patient and one aimed at a clinician currently read from the same voice, and nothing in the pack says they should differ.

## Aims

### A1 · 🚪 What the channel gates: three stages fire, three skip
- A1.1 · A reminder pin reads its gates and its bar from this pack instead of from memory.
  **Done when:** a venue pin for reminder records the three skipped stages and the light bar with `README.md` named as the source.

### A2 · 🔁 What the channel rewards: a rotating set, never one message
- A2.1 · A reminder draft is a rotating set, never a single message.
  **Done when:** a draft under this venue shows 3 to 5 variants whose motivation slot varies while the prompt and encouragement slots hold still.

### A3 · ❌ What desk-rejects a reminder design
- A3.1 · The refusals are checked before release rather than found in review.
  **Done when:** a draft's self-review records length, tone, variation, the question hook, and the advice frontmatter, closing the checklist's dropped hook.

### A4 · 🕳 What the pack does not know: the schedule is the intervention
- A4.1 · Every scheduling GAP in §4 is closed by the pack or ruled out of it.
  **Done when:** the Decision Now row is answered and each scheduling GAP carries either a pack line or the ruling that it lives per intervention.
- A4.2 · The two schema-demanded parts the folder lacks exist or are waived.
  **Done when:** `venue-reminder/exemplars/` holds at least one real artifact and the style-profile carries tone-by-audience rows, or JL waives each with the reason recorded.

## States

### Decision Now

- [ ] 🗣 Does the scheduling vocabulary go into the pack, or stay per intervention?
      📍 `§4` the GAP roster this ruling closes or reclassifies
      🔔 `Why now` the venue's identity is its trigger, and the pack records nothing about when a reminder fires
      ⭐ `A ·` extend `venue-reminder/README.md` with a scheduling block (anchor event, offset, escalation, stop rule), committing every reminder pin to declare them; CC recommends A because the channel's message is its time, and a pack recording only the text covers the wrong half
      `B ·` keep the pack content-only and let each intervention record its schedule in its own pitch, committing the pack to stay thin and every intervention to re-derive the vocabulary
      🛑 `Blocks` A4.1; the §4 scheduling GAPs cannot close until this is answered
      🤖 `If nobody answers` B, the pack stays as it is on disk today

### A1 · 🚪 What the channel gates: three stages fire, three skip
- ⬜ A1.1 · Not started. The stages block and `claims_settlement: light` sit in `README.md`; no pin has been checked against them from this page.

### A2 · 🔁 What the channel rewards: a rotating set, never one message
- ⬜ A2.1 · Not started. The rotation rule is stated twice (README constraints, drafting rule 1) and its only enforcement is the manual checklist.

### A3 · ❌ What desk-rejects a reminder design
- ⬜ A3.1 · Not started. The checklist sits at the end of `style-profile.md` and covers four of the five drafting rules; the question hook has no row.

### A4 · 🕳 What the pack does not know: the schedule is the intervention
- 🧠 A4.1 · Waiting on JL; the Decision Now row above holds the scheduling ruling.
- ⬜ A4.2 · Not started. `exemplars/` is absent on disk and `style-profile.md` carries no tone-by-audience rows (checked 260802).

## Files

- `../../../../application/venue/venue-reminder/README.md`
  The hub this page reads: the constraints, the stages block, the light bar, the 3-slot template, and the claims and draft mappings; a gate or budget change starts here.
- `../../../../application/venue/venue-reminder/style-profile.md`
  The voice examples, the five drafting rules, and the self-review checklist; a tone or rotation change starts here.
- `../../../../application/venue/_SCHEMA.md`
  What every venue pack must carry; §4 measures this pack against it.

## Glossary

- ⏱ **Anchor event**: the moment a reminder's clock starts, such as a prescription pickup or an enrollment date; the pack names the trigger kind (event-triggered) and never the event.
- ↔️ **Offset**: the gap between the anchor event and the first fire, such as three days after pickup; unrecorded in the pack.
- 📈 **Escalation**: the policy for an ignored reminder, whether it repeats, changes tone, or goes quiet; unrecorded in the pack.
- 🛑 **Stop rule**: when the rotating series ends for one recipient; unrecorded in the pack.
- ⚖️ **Settlement bar**: how much of the claims campaign must settle before artifact work, set per venue in `_SCHEMA.md`; this venue sets it to light.
- 🧱 **K/W entry**: a claims-ledger entry at the knowledge (K) or wisdom (W) rung; a template slot names one as its `claim_source`.

## Log

260802 · Opened as one of the QBv venue-pack pages, from `application/venue/venue-reminder/` read against `_SCHEMA.md`, with the desk-personality shape adapted from QBv1@paper. GAPs recorded: the scheduling vocabulary (anchor event, offset, escalation, stop rule) and the missing `exemplars/` and tone-by-audience rows in §4, plus the checklist's dropped question hook in §3; the scheduling ruling is parked with JL as the one Decision Now row.
