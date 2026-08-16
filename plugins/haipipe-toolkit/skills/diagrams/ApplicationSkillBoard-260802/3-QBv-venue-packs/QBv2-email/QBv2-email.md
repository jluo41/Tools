# email: the venue with a subject line and room to argue

state: 🔴 OPEN
owner: JL
method: state what the pack's two files record, audit them against `_SCHEMA.md`, and write a GAP where an answer is owed and absent

## Opening
What does the email venue pack know: what the channel gates, what it rewards, and what it requires of claims settlement, tone, and shape?
A venue pack is the folder a pinned venue is read from, and `venue-email/` is two files: gates and constraints in a README, voices in a style profile.
Email sits mid-ladder: the first venue that argues in sections, on the medium settlement bar.
Where the schema demands what the pack does not record, this page writes a numbered GAP rather than an invention.

**Where this page sits**: one page per venue pack in this group.
The shape follows QBv1@paper, the MISQ desk page on the paper board, with the journal desk adapted to a channel that has audiences instead of reviewers.
This page owns only what is true of `venue/venue-email/`.

**Covered elsewhere**: the seven sibling packs named in `_SCHEMA.md` (venue-sms, venue-push, venue-reminder, venue-checklist, venue-dashboard, venue-ui-card, venue-report) each get their own page.
The pin mechanics belong to the venue stage (`haipipe-application-venue`), not here.

**Why it matters**: the pinned venue decides which lifecycle stages fire and how deep claims must settle before an artifact ships.
Email is the transition venue: on the schema's eight-venue table it is the first that requires a narrative and the last that skips section-edit.

**What is thin**: the pack is two files, the `exemplars/` folder the schema promises does not exist on disk, and deliverability and compliance are recorded nowhere, so §5 carries five gaps and two of them are raised as decisions.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Inherited from the board's page contract**: the section order, the Opening split, and the sentence rules come from `haipipe-board-page` and `haipipe-board/ref/writing-rules.md` and are not restated here.

**A number may be stated, but never claimed**: a word budget, character cap, or section count appears only with its source named inline (a README constraints row, a style-profile line, or the schema's settlement block), never as this page's own claim.
The one measurement this page made itself, the roughly 70 to 80 word count of the two voice examples, is labelled as this page's own count wherever it appears.

**Say what the channel gates, not what it prefers**: a stage row or a checklist row decides work, and a tone adjective does not.

✅ `section-edit: skip`  ❌ `email likes a friendly tone`

**A missing answer is a GAP, never a paraphrase**: where the schema or the README's own mappings demand what no file records, §5 carries a numbered GAP row and nothing on this page fills it with invented doctrine.

## Diagram

**The pack at a glance**: two files, six gates, one bar, two voices.

```text
  📬 THE PACK    venue-email/ · README.md + style-profile.md
                 exemplars/ ── promised by _SCHEMA.md, absent on disk

  🚦 STAGES      seed req · claims req · pitch req · narrative req
                 display optional · section-edit skip

  ⚖️ SETTLEMENT  medium ── primaries supported or weak-with-caveat ·
                 load-bearing GAPs carry a campaign row

  📐 SHAPE       200-800 words · 3-5 sections · subject ≤ 60 chars
                 context → finding → recommendation → next steps

  🗣 VOICES      patient ── warm · clinician ── clinical
                 the style-profile tone rows ARE the audience axis

  🕳 GAPS        5 recorded in §5 · 2 raised as Decision Now rows
```

## Content

### 1 · What the channel gates: four stages on, one off

**The stage row, against its neighbours**: what fires when email is pinned, read off the schema's eight-venue table.

```text
  🚦 EMAIL        seed req · claims req · pitch req · narrative req
                  display optional · section-edit skip

  🪜 THE LADDER   sms / push / reminder    no narrative         · light
                  checklist                narrative optional   · medium
                  EMAIL ◀                  narrative required   · medium
                  ui-card                  + display required   · full
                  dashboard / report       everything required  · full

  📌 AT PIN       stages block ──▶ STATUS.md `stages_skipped` row
```

🚦 Establishes which lifecycle stages a pinned email intervention runs, and where email sits among the eight venues.

Pinning email keeps the always-required spine and adds one stage: seed, claims, and pitch are required at every venue, and email makes narrative required too [venue-email/README.md, Stage requirements; _SCHEMA.md, Stage requirements block].
The pin lands mid-spine: seed and claims are venue-free and already exist when email is pinned, and pitch runs after the pin [_SCHEMA.md, Stage requirements block].
display is optional and the README says exactly when it fires: an email carrying data (a chart, a table, a KPI) writes a display map, and a pure-text email skips the stage [venue-email/README.md, Display mapping].
section-edit is skip, so an email is drafted whole against the narrative arc rather than section by section [venue-email/README.md, Stage requirements].
On the schema's summary table email is the first venue that requires a narrative and the last that skips section-edit, which is what the title's room to argue means: the README grants "more room for evidence-backed argumentation than SMS/push", in sections, without per-section machinery [_SCHEMA.md, Stage requirements summary; venue-email/README.md line 4].
Because narrative fires, email carries no `template:` block: the fixed-slot template is the schema's replacement for a skipped narrative, and email's structure comes from the narrative stage instead [_SCHEMA.md, Venue template].
At pin time `haipipe-application-venue` translates the stages block into the STATUS.md `stages_skipped` row, so the gate is applied by the pin rather than recalled later [_SCHEMA.md, Stage requirements block].

### 2 · The settlement bar: medium, and what it asks of the ledger

**Medium, between its neighbours**: the bar the claims check applies before email artifact work, quoted from the schema.

```text
  ⚖️ light       claims tied to a named K/W or common knowledge ·
                 GAPs allowed if not load-bearing
  ⚖️ MEDIUM ◀    primary claims supported or weak-with-caveat ·
                 load-bearing GAPs have a campaign row in 1-probes/
  ⚖️ full        primary claims supported by judged answers ·
                 load-bearing GAPs settled

  🔍 THE CHECK   each section's core statement ──▶ one K/W entry
                 no backing ──▶ flag the gap
```

⚖️ Establishes the settlement bar as medium, and what that bar concretely refuses.

The claims ledger is venue-free and keeps one shape everywhere; the venue only sets how much of the evidence campaign must settle, and email sets it to medium [_SCHEMA.md, Claims settlement; venue-email/README.md, claims_settlement].
Medium means the primary claims are supported or weak-with-caveat, and every load-bearing GAP carries a campaign row: an open question in `1-probes/` [_SCHEMA.md, Claims settlement].
The README's own mapping is a select plus gap check: each section's core statement should trace to a K/W entry, and a section with no backing flags the gap [venue-email/README.md, Claims mapping].
Against light, a primary claim must actually be supported or carry a caveat rather than merely be tied to a named entry [_SCHEMA.md, Claims settlement].
Against full, nothing has to be judged: the campaign row must exist, not its answer [_SCHEMA.md, Claims settlement].

### 3 · The shape: a letter arc behind a 60-character subject line

**The letter, measured**: every format number the pack records, each with its source row.

```text
  ✉️ SUBJECT     ≤ 60 chars · specific ── "Important Update" is the
                 pack's own counter-example
  📏 LENGTH      200-800 words · "(audience-dependent)" ── no
                 per-audience row exists
  🧱 SECTIONS    3-5 · context → finding → recommendation → next steps
  🔗 LINKS       allowed · descriptive anchor text
  🖼 IMAGES      optional inline · charts, diagrams
  📋 BULLETS     for actionable items
```

📐 Establishes the artifact's fixed frame: one subject line, one arc, and the constraint rows a draft is measured against.

The subject line is at most 60 characters and specific, and the pack names its own counter-example: not "Important Update" [venue-email/README.md, Constraints; venue-email/style-profile.md, Drafting rules].
The body runs 200 to 800 words in 3 to 5 sections [venue-email/README.md, Constraints].
The sections follow the narrative stage's letter arc in reader order: context (why you are receiving this), finding (what the evidence shows), recommendation (what to do), next steps (what happens next) [venue-email/README.md, Narrative mapping].
Links are allowed with descriptive anchor text, inline images are optional, and actionable items go in bullet lists [venue-email/README.md, Constraints; venue-email/style-profile.md, Drafting rules].
The draft is the subject line plus sections following that arc, with tone per audience profile and citations per audience rules [venue-email/README.md, Draft mapping].
The 200-word floor is contradicted by the pack's own voice examples, which is §5.1 and the first Decision Now row.

### 4 · The voice: one finding, two audiences

**One finding, two readers**: the pack's two voice examples, and what flips between them.

```text
  🧑 PATIENT      warm · "Hi [Name]" · ~80 words (this page's count) ·
                  zero citations · closes "We're here to support you"
  🩺 CLINICIAN    clinical · "Dr. [Name]" · ~70 words (this page's
                  count) · one inline claim id "(C3)" · system sign-off

  🔀 WHAT FLIPS   greeting · evidence depth · citation form · sign-off
  🔒 WHAT HOLDS   subject ≤ 60 · arc order · bullets for actions
```

🗣 Establishes the audience axis as the style-profile's two examples, because the schema says those tone rows are the axis.

Venue and audience are orthogonal but live in one pack: the venue determines what the output looks like, the audience determines how it sounds, and the style-profile's tone-by-audience rows are the audience axis with no separate directory [_SCHEMA.md, Audience].
The patient voice is warm and body-first: a first-name greeting, a plain-language reason ("helps keep your levels steady"), three bulleted actions, and a care-team sign-off [venue-email/style-profile.md, Patient email].
The clinician voice is clinical and evidence-first: a count in the subject line ("4 patients flagged"), findings as measured bullets, recommended actions with a dashboard link, and a system signature [venue-email/style-profile.md, Clinician email].
The clinician example carries the only citation form the pack shows anywhere: an inline parenthetical claim id, "based on timing analysis (C3)", while the patient example carries no citation at all [venue-email/style-profile.md, Voice examples].
That form is shown rather than stated as a rule, which is §5.2.
What holds across both audiences is the frame: a specific subject line, the arc order, and bullets for whatever the reader is asked to do [venue-email/style-profile.md, Drafting rules].

### 5 · What fails the desk, and what the pack cannot answer

**The desk and its holes**: the recorded failure conditions, then the five gaps.

```text
  ⛔ FAILS THE CHECK   subject > 60 chars or vague · outside 200-800 ·
                       sections off the arc · a claim without its K/W
                       citation · adopted_A / declined_A missing ·
                       claims ledger under the medium bar

  🕳 GAP 5.1  word floor    both examples ~70-80w, under the 200 floor
  🕳 GAP 5.2  citations     "format per audience" required, stated nowhere
  🕳 GAP 5.3  budget split  "(audience-dependent)" with no per-audience row
  🕳 GAP 5.4  exemplars/    promised by _SCHEMA.md · absent on disk
  🕳 GAP 5.5  delivery      deliverability + compliance recorded nowhere
```

🕳 Establishes what the venue's check can already refuse, then names the five answers the pack does not have instead of inventing them.

Email has no human editor, so its desk is the venue check: the style-profile's self-review checklist on the artifact, and the settlement gate under it [venue-email/style-profile.md, Self-review checklist; _SCHEMA.md, Claims settlement].
A draft fails on any recorded row: a subject over 60 characters or a vague one, a body outside 200 to 800 words, sections that do not follow the arc, a claim that does not cite K/W, or missing `adopted_A / declined_A` frontmatter [venue-email/style-profile.md, Self-review checklist].
Under the artifact, the claims gate fails the stage when a primary claim is neither supported nor weak-with-caveat, or a load-bearing GAP has no campaign row [_SCHEMA.md, Claims settlement].

#### 5.1 · GAP: the word floor against the pack's own examples
(the README floor and the style-profile voice cannot both be imitated)
The constraints row says 200 to 800 words and the checklist enforces that range [venue-email/README.md, Constraints; venue-email/style-profile.md, Self-review checklist].
Both voice examples run about 70 to 80 words by this page's own count, under half the floor [venue-email/style-profile.md, Voice examples].
No file says whether the floor binds or the examples do, so the ruling is raised as the first Decision Now row.

#### 5.2 · GAP: a citation format required per audience and stated for none
(the draft mapping demands it; the pack only shows one instance)
The draft mapping says citations per audience rules, and the checklist requires every claim to cite K/W in a per-audience format [venue-email/README.md, Draft mapping; venue-email/style-profile.md, Self-review checklist].
No file states those rules: the clinician example shows one parenthetical claim id, "(C3)", and the patient example shows none.
Until a rule is written, the two examples are the only guidance, read off rather than stated.

#### 5.3 · GAP: an audience-dependent budget with no per-audience number
(a shared range and a promise, not a rule)
The length row says 200-800 words "(audience-dependent)" [venue-email/README.md, Constraints].
Which audience gets which end of the range is recorded nowhere.

#### 5.4 · GAP: the exemplars the schema promises are not on disk
(the pack layout owes a folder this pack does not have)
The schema's pack layout includes `exemplars/`, real artifacts to pattern-match, and its draft mapping reads style from them [_SCHEMA.md, pack layout and Lifecycle mappings].
`venue-email/` holds two files, README.md and style-profile.md, and no exemplar file exists on disk.
Whether to collect exemplars, amend the schema, or leave the hole is the second Decision Now row.

#### 5.5 · GAP: deliverability and compliance, recorded nowhere
(nothing in the pack governs the send itself)
No row in either file covers sender identity, send time, spam triggers, an unsubscribe or opt-out line, or what may appear in a subject line beyond its length.
The patient voice example places `[Medication]` in its subject line and closes without an opt-out, and the pack records no rule either way [venue-email/style-profile.md, Patient email].
This page records the hole rather than writing compliance doctrine into a venue pack; A5.4 holds the target.

## Aims

### A1 · 🚦 What the channel gates: four stages on, one off
- A1.1 · The stage row is applied by the pin, not recalled by a person.
  **Done when:** an intervention pinned to email shows the README's stages block translated into its STATUS.md `stages_skipped` row, unedited by hand.

### A2 · ⚖️ The settlement bar: medium, and what it asks of the ledger
- A2.1 · The medium bar is what the claims check actually applies before email artifact work.
  **Done when:** an email intervention's claims gate shows each primary claim supported or weak-with-caveat and each load-bearing GAP with its campaign row in `1-probes/`.

### A3 · 📐 The shape: a letter arc behind a 60-character subject line
- A3.1 · Every recorded number is checked on the draft, not remembered at review.
  **Done when:** an email draft records its measured subject length, word count, and section count against the README's constraint rows.

### A4 · 🗣 The voice: one finding, two audiences
- A4.1 · The audience is pinned before drafting, since it flips greeting, evidence depth, citation form, and sign-off.
  **Done when:** an email draft names its audience and the voice example it imitates.

### A5 · 🕳 What fails the desk, and what the pack cannot answer
- A5.1 · The word-budget contradiction is ruled, and the pack's two records agree with the ruling.
  **Done when:** the first Decision Now row is closed and README.md and style-profile.md are consistent under the chosen option.
- A5.2 · The per-audience rows exist: a citation format and a word budget stated per audience instead of read off the examples.
  **Done when:** the pack states the citation form and the budget for the patient and the clinician audiences in a constraints or style row.
- A5.3 · The exemplars promise is settled: filled, waived on this page, or amended in the schema.
  **Done when:** the second Decision Now row is closed and either exemplar files exist under `venue-email/exemplars/`, `_SCHEMA.md` is amended, or the leave-it ruling is recorded here.
- A5.4 · Deliverability and compliance have a recorded owner.
  **Done when:** the pack records send rules (opt-out, sender identity, subject-line content), or a dated line on this page names what owns them outside the pack.

## States

### Decision Now
- [ ] 🗣 Which binds a short email: the 200-word floor, or the pack's own 80-word voice examples?
      📍 `§5.1`, raised there; the constraint itself sits in §3.
      🔔 `Why now` a drafter who imitates either voice example fails the self-review checklist on the pack's own numbers.
      `A ·` the floor binds: rewrite both style-profile examples past 200 words, so imitation and the checklist agree.
      `B ·` the examples bind: change the constraint row and the checklist to `≤ 800 words`, accepting very short emails.
      ⭐ `C ·` both stand with roles named: one label line in style-profile.md marks the examples voice-only while the 200-800 budget governs finished artifacts; the smallest edit that makes both records true.
      🛑 `Blocks` the first email draft's self-review, which cannot pass the checklist and imitate the examples at once.
      🤖 `If nobody answers` C.

- [ ] 🗣 Fill `exemplars/`, or amend the schema that promises it?
      📍 `§5.4`.
      🔔 `Why now` this page is the first audit of venue-email against `_SCHEMA.md`, and the missing folder is its one layout violation.
      `A ·` collect exemplars: real sent emails land under `venue-email/exemplars/`, and the draft stage gains artifacts to pattern-match.
      `B ·` amend `_SCHEMA.md`: mark `exemplars/` optional for message venues, which changes the contract for all eight packs.
      ⭐ `C ·` leave both and let this page carry the gap, since the style-profile's two examples already give draft something to imitate; the cheapest option until a real email intervention needs more.
      🛑 `Blocks` nothing; draft runs off style-profile.md today.
      🤖 `If nobody answers` C.

### A1 · 🚦 What the channel gates: four stages on, one off
- ⬜ A1.1 · Not started; the stage row is recorded in the README and on this page, and no pinned intervention has been checked against it from here.

### A2 · ⚖️ The settlement bar: medium, and what it asks of the ledger
- ⬜ A2.1 · Not started; the bar is quoted from `_SCHEMA.md` and no email claims gate has been read against it from this page.

### A3 · 📐 The shape: a letter arc behind a 60-character subject line
- ⬜ A3.1 · Not started; no email draft exists to measure.

### A4 · 🗣 The voice: one finding, two audiences
- ⬜ A4.1 · Not started; the two voice examples are the pack's only audience record.

### A5 · 🕳 What fails the desk, and what the pack cannot answer
- 🧠 A5.1 · Waiting on JL; the first Decision Now row carries the options.
- ⬜ A5.2 · Not started; the only citation form on record is the clinician example's "(C3)".
- 🧠 A5.3 · Waiting on JL; the second Decision Now row carries the options.
- ⬜ A5.4 · Not started; no file in the pack mentions opt-out, sender identity, send time, or subject-line content limits.

## Files

- `../../application/venue/venue-email/README.md`
  The hub: constraints, stage gates, the settlement bar, and the lifecycle mappings; the first file to edit when this venue's rules change.
- `../../application/venue/venue-email/style-profile.md`
  The two voice examples, the drafting rules, and the self-review checklist; edit here when the tone or the desk's checklist changes.
- `../../application/venue/_SCHEMA.md`
  What every venue pack owes: the stages block, the settlement definitions, and the pack layout this page audits venue-email against.

## Glossary

- 📖 **K/W entry**: the evidence anchor an email section's core statement must trace to ("Each section's core statement should trace to a K/W entry" [venue-email/README.md, Claims mapping]); no file in this pack expands the abbreviation.
- ⚖️ **Settlement bar**: how much of the claims campaign must settle before artifact work, one of light, medium, or full [_SCHEMA.md, Claims settlement].
- 🪜 **The ladder**: this page's word for the schema's two parallel orderings, venues by how many stages fire and settlement by light, medium, full; email is mid-way on both.
- 🗂 **adopted_A / declined_A**: two frontmatter rows the self-review checklist requires on a draft [venue-email/style-profile.md]; the pack requires them and defines them in no file.
- 🏛 **Desk**: this page keeps QBv1@paper's word for the place an artifact is accepted or refused; email's desk is the venue check rather than an editor's inbox.

## Log

260802 · Opened from `venue-email/` (README.md and style-profile.md, the pack's only two files on disk) audited against `_SCHEMA.md`, with the page shape adapted from QBv1@paper; five gaps recorded in §5 and two decisions raised in States.
