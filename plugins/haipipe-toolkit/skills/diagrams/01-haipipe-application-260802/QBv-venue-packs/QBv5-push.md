# push: the venue that interrupts, and pays for it

state: 🔴 OPEN
owner: JL
method: read the two pack files against the schema, state what the channel gates, rewards, and refuses in the pack's own numbers, and record what it lacks as GAP items for JL to place

## Opening

What does the push-notification venue pack know: what does this channel gate, reward, and require?
A push is a title and a body that light a phone uninvited, so it spends the reader's attention before one word lands.
The pack at `venue-push/` is two small files, and this page records what they hold: which stages fire, the two-slot template, the light claims bar, and three voices.
It also records what they lack as GAP items, because the pack never prices the interruption itself.

**Where this page sits**: one pack page per channel in `QBv-venue-packs`; the short venues nearest to push, the SMS and reminder packs, own their own pages, and this page owns only what is true of `venue-push/`.

**Why it matters**: pinning a venue decides which lifecycle stages fire and how deep claims must settle, so every intervention pinned to push inherits exactly what this page records, silences included.

**Shape precedent**: QBv1@paper wrote the first pack page in this voice, saying what a desk gates and refuses in its own numbers, for a 50-page manuscript outlet; this page adapts that voice to a channel whose whole artifact is about 150 characters.

**Covered elsewhere**: the schema all eight packs answer to lives in `_SCHEMA.md` and is read here only as the yardstick for §5's GAP items.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited**: the page grammar, the section order, and the sentence rules come from the board's page contract and its writing rules, and are not restated here.

**A number is the pack's, never this page's**: a character budget or an entry ceiling appears only with its source named inline (a README.md block or a style-profile.md rule), never as this page's own claim.

**Say what the pack refuses or lacks, never what push "should" do**: a GAP is recorded and routed to an Aim or to JL, not filled with an invented rule.

✅ `the pack names no send-window row`  ❌ `push should cap sends at one per day`

## Diagram

**The push pack at a glance**: what fires, what the artifact is, and where the pack goes silent.

```text
  📣 THE ARTIFACT   title ≤ 50 chars + body ≤ 100 · one tap · deep link

  🚦 GATES      seed ✓ · claims ✓ (light · ≤ 2 K/W) · pitch ✓
  ⛔ SKIPPED    narrative · display · section-edit
  🎰 TEMPLATE   title ← primary claim · body ← action claim (W)
  🗣 VOICES     patient urgent · patient motivational · clinician alert
  ❌ REFUSES    opt-out in body · a second tap · budget overruns
  🕳 SILENT ON  exemplars/ · timing + frequency caps · deep-link targets
```

## Content

### 1 · What the channel gates

**Three stages fire, three are replaced**: the skip list is the venue's first decision, made before any word is drafted.

```text
  🚦 REQUIRED   seed · claims · pitch
  ⛔ SKIP       narrative · display · section-edit
  🎰 STAND-IN   the two-slot template (§2)
  📌 AT PIN     stages: block → STATUS.md stages_skipped row
```

🚦 Establishes push as a minimum-lifecycle venue: the three always-required stages fire, and the template stands in for everything else.

The pack's `stages:` block requires seed, pitch, and claims, and skips narrative, display, and section-edit [venue-push/README.md, Stage requirements].
Seed and claims are venue-free and already exist when push is pinned, so the spine runs seed, claims, pin, pitch [_SCHEMA.md, Stage requirements block].
For a venue that skips those three stages, the venue template replaces them with a fixed output structure, and push's structure is the two slots in §2 [_SCHEMA.md, Venue template].
At pin time `haipipe-application-venue` translates the block into the STATUS.md `stages_skipped` row, so the skip list travels by machinery rather than by memory [_SCHEMA.md, Stage requirements block].

### 2 · What it rewards: two slots and a light bar

**The whole artifact is two claim-fed slots**: about 150 characters, one tap, and at most two ledger entries behind them.

```text
  🎰 TEMPLATE   [venue-push/README.md, Venue template]
     title   ~50 chars  · hook + urgency        ← primary claim
     body    ~100 chars · benefit + action hint ← action claim (W)

  📏 CEILINGS   title ≤ 50 · body ≤ 100   [Constraints]
  👆 ACTION     one tap · deep link to an app screen
  🖼 MEDIA      optional image · 1:1 ratio · ≤ 1MB

  ⚖️ CLAIMS     light bar · 2 K/W entries max
                one for the hook · one for the action
```

🎰 Establishes the reward shape: a hook the primary claim can fill, an action the ledger can name, and no room for a third argument.

The title's job is hook plus urgency in about 50 characters, fed by the primary claim; the body's job is benefit plus an action hint in about 100, fed by an action claim, W in the pack's own notation [venue-push/README.md, Venue template].
The constraints block makes those budgets hard: title at most 50 characters, body at most 100, a single tap that deep-links to an app screen, and an optional square image under 1MB [venue-push/README.md, Constraints].
Claims settle at light, the schema's lowest bar: every claim the artifact leans on is tied to a named K/W entry or to common knowledge, and a GAP is allowed when it is not load-bearing [_SCHEMA.md, Claims settlement].
Push narrows even that: 2 K/W entries max, one for the hook and one for the action [venue-push/README.md, Claims mapping].
That ceiling is the pack's whole evidence campaign, so a case that cannot be said as one hook claim and one action claim is a retarget signal rather than a drafting problem.
The draft mapping compresses the same rule into two sentences: the title grabs attention, and the body gives one reason plus one action [venue-push/README.md, Draft mapping].

### 3 · Who hears it, and how it sounds

**Three voice rows are the whole audience axis**: the schema folds audience into the pack, and push's profile answers with three worked examples.

```text
  🗣 VOICES   [venue-push/style-profile.md, Voice examples]
     patient · urgent         due date + name + medication + tap prompt
     patient · motivational   streak count + next due date
     clinician · alert        at-risk count + tap to the panel

  🧭 AXIS     venue → structure · audience → tone   [_SCHEMA.md, Audience]
  ☑️ CHECK    tone matches audience · adopted_A / declined_A in frontmatter
```

🗣 Establishes the audience rule as example-borne: the three rows are the only tone guidance the pack gives, and the checklist tests against them.

Venue and audience are orthogonal but coupled, and both live in this pack: the venue determines what the output looks like, the audience determines how it sounds, and the style profile's tone-by-audience rows ARE the audience axis [_SCHEMA.md, Audience].
Push's profile carries three rows: a patient urgent voice built on a due date, the person's name and medication, and a tap prompt; a patient motivational voice built on a streak count and the next due date; and a clinician alert voice built on an at-risk count and a tap to the panel [venue-push/style-profile.md, Voice examples].
The profile states no tone rule beyond the rows themselves, so its self-review line "tone matches audience" is checked against an example, not a definition [venue-push/style-profile.md, Self-review checklist].
The same checklist requires `adopted_A / declined_A` in the draft's frontmatter, which ties every push artifact back to the advice entries it took or turned down [venue-push/style-profile.md, Self-review checklist].

### 4 · What desk-rejects a push

**The refusals are implied, not listed**: this pack has no taste file, so its rejections are read off its own four drafting rules and two ceilings.

```text
  ❌ REFUSED
     title over 50 chars · body over 100
     a second tap · a tap with no named deep-link target
     opt-out text in the body (the OS owns settings)
     a case needing more than 2 K/W entries
     anything needing narrative, display, or section-edit

  ⚠️ SOURCE   drafting rules 1-4 + the stages and claims blocks
```

❌ Establishes what turns a push intervention away, with each refusal traced to the pack line that implies it.

A title over 50 characters or a body over 100 breaks the first two drafting rules and the constraints block behind them [venue-push/style-profile.md, Drafting rules; venue-push/README.md, Constraints].
A second tap action, or a tap whose deep-link target is unnamed, breaks rule 3 and fails the checklist's "deep link target specified" box [venue-push/style-profile.md, Drafting rules and Self-review checklist].
Opt-out text in the body is refused twice over: the draft mapping and rule 4 both hand it to the OS notification settings [venue-push/README.md, Draft mapping; venue-push/style-profile.md, Drafting rules].
A case that needs more than two load-bearing K/W entries has no slot to land in, since the claims mapping caps the campaign at one hook entry and one action entry [venue-push/README.md, Claims mapping].
An intervention that needs a narrative arc, display units, or sectioned editing is refused by the stages block itself, because the venue skips all three [venue-push/README.md, Stage requirements].
None of this is a stated desk list, so the refusals hold only as firmly as the rules they are read from.

### 5 · GAP: what is demanded of the pack and not held

**Three silences, recorded rather than filled**: each is an answer the schema, the channel, or the pack's own checklist demands and the two files do not hold.

```text
  🕳 GAP-1   exemplars/       schema pack shape demands it · folder absent
  🕳 GAP-2   timing + caps    the channel's defining cost · no constraint row
  🕳 GAP-3   deep-link menu   checklist demands a target · pack names none
```

🕳 Establishes the pack's three silences as GAP items, each owned by an Aim below instead of being invented on this page.

#### 5.1 · GAP-1: no exemplars/ folder
(the schema's pack shape demands one and the folder is absent)
The schema's uniform pack is README.md, style-profile.md, and exemplars/ holding real artifacts to pattern-match, and venue-push ships only the first two [_SCHEMA.md; the venue-push/ folder listing].
Until the folder exists there is no real push to pattern-match, so the three synthetic voice rows in §3 carry the whole style burden.

#### 5.2 · GAP-2: the interruption is unpriced
(no send-window, frequency-cap, or quiet-hours row anywhere in the pack)
Push fires uninvited, and the send itself is the one cost the constraints block does not price: it caps characters and image weight and says nothing about when or how often a push may fire [venue-push/README.md, Constraints].
Where that cap should live, in the pack for every push intervention or in each intervention's own case, is a design ruling and it is JL's; the Decision Now row in States carries the options.

#### 5.3 · GAP-3: the deep link has no menu
(the checklist demands a target and the pack names no screen)
The action is a single tap deep-linking to an app screen, and the checklist requires every draft to specify its target [venue-push/README.md, Constraints; venue-push/style-profile.md, Self-review checklist].
The pack names no app and no screen anywhere, so every draft must source its target from the intervention rather than from the venue.

## Aims

### A1 · 🚦 What the channel gates
- A1.1 · The skip list reaches STATUS.md through the pin machinery, not from memory.
  **Done when:** a pinned push intervention's `stages_skipped` row matches the pack's `stages:` block.

### A2 · 🎰 What it rewards: two slots and a light bar
- A2.1 · Every push draft is measured against both character ceilings before its gate.
  **Done when:** a draft records its title and body counts against 50 and 100.
- A2.2 · The claims CHECK applies the light bar with push's 2-entry ceiling.
  **Done when:** a push claims check names one hook K/W and one action K/W and refuses a third load-bearing entry.

### A3 · 🗣 Who hears it, and how it sounds
- A3.1 · The voice row is chosen with the audience, not defaulted.
  **Done when:** a push draft names which of the three rows it imitates.

### A4 · ❌ What desk-rejects a push
- A4.1 · The implied refusals are run as the draft's self-review, and recorded.
  **Done when:** a draft records a completed run of the five-box checklist.

### A5 · 🕳 GAP: what is demanded of the pack and not held
- A5.1 · The pack gains an exemplars/ folder with at least one real push artifact.
  **Done when:** `venue-push/exemplars/` exists and the style profile points at its contents.
- A5.2 · Timing and frequency have an owner: the pack or the intervention.
  **Done when:** JL's Decision Now ruling is recorded and the chosen home carries the cap.
- A5.3 · The deep-link target's source is settled: a pack-level screen menu, or a requirement pinned at the intervention's seed.
  **Done when:** a push draft can fill the checklist's target box from a named place rather than ad hoc.

## States

### Decision Now
- [ ] 🗣 Where does the interruption cap live: in the pack, or in each intervention?
      📍 `§5.2` the GAP it settles
      🔔 the constraints block prices characters and image weight but not the send itself, and push is the shortest venue that fires uninvited
      ⭐ `A ·` add a timing block (send window, frequency cap, quiet hours) to `venue-push/README.md`, so every push intervention inherits one cap; CC recommends A because the interruption cost is a property of the channel, not of one intervention
      `B ·` leave the pack as-is and require each intervention's seed or claims to state its own cap, so the cost is argued per case
      🛑 `Blocks` A5.2, and any push draft's check against an interruption budget
      🤖 `If nobody answers` B in effect by default, since a draft can ship today with no cap anywhere

### A1 · 🚦 What the channel gates
- ⬜ A1.1 · Not started. No push intervention is pinned, and the block sits unread in the pack.

### A2 · 🎰 What it rewards: two slots and a light bar
- ⬜ A2.1 · Not started. The ceilings are recorded twice, in Constraints and in the drafting rules, and nothing measures a draft against them.
- ⬜ A2.2 · Not started. The light bar is schema prose and the 2-entry ceiling is one pack line; no check applies either.

### A3 · 🗣 Who hears it, and how it sounds
- ⬜ A3.1 · Not started. Three rows exist and nothing records a choice.

### A4 · ❌ What desk-rejects a push
- ⬜ A4.1 · Not started. The checklist exists in the style profile and no draft has run it.

### A5 · 🕳 GAP: what is demanded of the pack and not held
- ⬜ A5.1 · Not started. The folder is absent; the pack ships two files.
- 🧠 A5.2 · Waiting on JL: the Decision Now row above.
- ⬜ A5.3 · Not started. The checklist demands the box and no named place fills it.

## Files

- `../../application/venue/venue-push/README.md`
  The pack's hub: the constraints, the stages block, the light settlement, the two-slot template, and the claims and draft mappings; a change to what push gates starts here.
- `../../application/venue/venue-push/style-profile.md`
  The three voice rows, the four drafting rules, and the five-box self-review checklist; a change to how push sounds starts here.
- `../../application/venue/_SCHEMA.md`
  What every venue pack owes; the yardstick §5's GAP items are measured against.

## Glossary

- 📏 **Light settlement**: the schema's lowest claims bar: every claim the artifact leans on is tied to a named K/W entry or to common knowledge, and a GAP is allowed when it is not load-bearing.
- 🧾 **K/W entry**: a knowledge or wisdom row in the intervention's venue-free claim ledger; push allows at most two, one feeding the title's hook and one feeding the body's action.
- 🔗 **Deep link**: the address a push's single tap opens, pointing at one specific app screen rather than the app's front door.
- 🕳 **GAP**: an answer the pack is asked for and does not hold, recorded on this page instead of invented.

## Log

260802 · Opened with the QBv venue-pack pages, from the two files under `application/venue/venue-push/` read against `_SCHEMA.md`; the missing exemplars/ folder, the unpriced interruption cost, and the unnamed deep-link targets recorded as GAP-1 to GAP-3, and the cap's home raised to JL as the page's one Decision Now.
