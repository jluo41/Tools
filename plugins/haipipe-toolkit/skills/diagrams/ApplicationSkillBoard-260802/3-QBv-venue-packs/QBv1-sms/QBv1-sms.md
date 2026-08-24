# sms: the venue where one sentence carries the whole intervention

state: 🔴 OPEN
owner: JL

## Opening

The SMS channel gives an intervention exactly 160 characters per segment to establish trust, state a benefit, demand one action, and reassure the recipient — and narrative, display, and section-edit stages are all skipped because none of that structure fits a message shorter than a tweet.
What are the channel's hard gates, and what does the light-settlement bar let through?

**Where this page sits**: this is one venue pack in `QBv`, one page per channel.
A neighbouring page would cover a different channel, such as push notifications (`venue-push`) or email (`venue-email`), each of which owns a different structure budget and a different claims-settlement depth.
This page owns only what is true of `venue-sms/` and is not a comparison across venues.

**Why it matters**: the SMS venue is the default channel for patient-facing interventions in this repo's DrFirst work, so its gates on length, tone, and claims settlement are the first filter a claim must survive before any artifact is drafted.
A claim that fits the knowledge base but cannot compress into ~60 characters for the benefit slot has nowhere to land in this channel.

**What is unread by any lifecycle run**: the style-profile's self-review checklist and the artifact frontmatter schema exist in the pack but no stage gate currently reads them programmatically; they are carried as GAP items in the Content below.


## Diagram

**SMS lifecycle and slot budget**: which stages fire, which skip, and where the 160-character budget lands.

```text
  ⚙️ LIFECYCLE
     seed ──▶ claims (light) ──▶ pitch ──▶ draft
     narrative  SKIP
     display    SKIP
     section-edit  SKIP

  📐 4-SLOT TEMPLATE  (≤ 160 chars total, prefer 1 segment)
     greeting   ~30 chars   identity + warmth       claim_source: personalization
     benefit    ~60 chars   value proposition       claim_source: K/W primary claim
     CTA        ~50 chars   action + deadline       claim_source: action claim (W)
     close      ~20 chars   reassurance + opt-out   claim_source: standard

  👤 AUDIENCE AXIS
     patient    → warm · plain · 6th-grade · no C-id in body
     clinician  → precise · clinical · inline C-id

  ❌ DESK-REJECT SIGNALS
     >160 chars without justification for a 2nd segment
     CTA absent or non-specific ("talk to your doctor")
     jargon in patient body
     unanchored factual claim not in K/W or common knowledge
     opt-out absent

  ⚠️ GAPS (pack says, no stage reads)
     self-review checklist
     artifact frontmatter schema
```


## Content

### 1 · Channel gates: what SMS enforces before any claim is asked

**Hard limits, from the channel itself**: what is structurally non-negotiable.

```text
  📏 LENGTH      ≤ 160 chars per segment; prefer 1 segment
                 2-segment max = 320 chars total
  🔤 LANGUAGE   plain; 6th-grade reading level for patient audience
  🔗 LINKS       short URL only (≤ 30 chars)
  👤 PERSON      patient name + medication name if available
  📢 CTA         exactly one; specific and actionable
  🛑 OPT-OUT     required (STOP keyword or equivalent)
```

The 160-character ceiling is a channel limit, not a style preference.
A message that exceeds one segment costs more to send, may split at an arbitrary byte boundary on some carriers, and raises opt-out rates.
The pack's hard rule is to prefer one segment and justify any second one explicitly.

#### 1.1 · What the length constraint does to claims
(the 160-character ceiling is the load-bearing gate for every downstream stage)
The benefit slot carries ~60 characters.
A primary claim that requires a qualifier, a caveat, or a secondary mechanism to be accurate does not fit.
The light claims-settlement bar means a claim may be "common knowledge" without a K/W entry — but it must still compress.
A claim that is well-settled in the knowledge base but cannot be stated in plain language at ~60 characters is not a gap in settlement; it is a gap in channel fit, and the correct action is to change the claim's phrasing at the pitch stage, not to expand the budget.

#### 1.2 · Lifecycle stages that fire and stages that skip
(the stage block in `venue-sms/README.md` is the gate list)
seed, claims, and pitch are required for every venue and fire here.
narrative, display, and section-edit are skipped: the 4-slot template replaces them.
The K/W-to-slot mapping happens at draft, not at claims.
The claims stage for this venue applies the light-settlement bar: every claim the artifact leans on must be tied to a named K/W entry or flagged as common knowledge; load-bearing gaps need a campaign row in `1-probes/` but do not block the gate.

### 2 · The 4-slot template: how the 160 characters are divided

**Slot budget and claim sources**: what each slot owes and where its content comes from.

```text
  📐 SLOT BREAKDOWN
     greeting   ~30 chars   job: establish identity + warmth
                            source: personalization (name, medication)
     benefit    ~60 chars   job: state the value proposition
                            source: primary claim from K/W
     CTA        ~50 chars   job: specific action + deadline
                            source: action claim from W layer
     close      ~20 chars   job: reassurance or opt-out
                            source: standard phrase
```

Each slot is one sentence or phrase.
The total must stay at or under 160 characters for a single-segment message.
The greeting and close are the most compressible; the benefit and CTA are not, because compressing them removes the claim and the action.

#### 2.1 · Patient voice vs clinician voice
(tone is the audience axis, not a separate slot)
For a patient audience: warm, plain language, 6th-grade reading level, no C-ids visible in the body.
For a clinician audience: precise, clinical terms are permitted, inline C-ids are expected.
The same 4-slot template applies to both; only the register changes.
Voice examples are in `venue-sms/style-profile.md`: the warm patient example leads with the recipient's name and medication, while the clinician example leads with a count of patients and a risk flag.

**2.1.1 · Patient warm example** (from `style-profile.md`)
```
Hi [Name], your [Medication] refill is due in 2 days.
Refilling on time helps keep your levels steady. Reply
REFILL to start or call [PharmacyPhone]. Reply STOP to
opt out.
```

**2.1.2 · Clinician concise example** (from `style-profile.md`)
```
[ProviderName]: 12 patients in your panel have refills
due within 72h. 4 are high-risk for lapse (C3). Review
list: [DashboardURL].
```

#### 2.2 · Personalization variables the pack names
(variables available in the slot template)
`[Name]`, `[Medication]`, `[PharmacyPhone]`, `[ShortURL]`, `[ProviderName]`, `[DashboardURL]`.
These are the named variables in `style-profile.md`; the data pipeline must supply them or the draft cannot be instantiated.

**GAP**: the pack does not declare what happens when a personalization variable is unavailable (e.g. medication name absent): whether to fall back to a generic noun, to skip the greeting slot content, or to block the artifact.
This is a GAP the `_SCHEMA.md` requires the pack to answer, and it does not.

### 3 · Claims settlement: what "light" means for this channel

**The light-settlement bar**: what it allows and what it still excludes.

```text
  📊 SETTLEMENT LEVEL    light
  ✅ ALLOWED             claim tied to named K/W entry
                         claim flagged as "common knowledge"
                         load-bearing GAP with campaign row in 1-probes/
  ❌ EXCLUDED            unanchored factual claim that is load-bearing
                           and has no K/W entry or probe row
  🔁 PROCESS             no probe planning required at claims stage
                         if KB lacks coverage: use common knowledge
                           OR trigger an ask session first
```

Light settlement does not mean claims are unverified.
It means the bar is lower: primary claims need to be supported or flagged as weak-with-caveat, but a gap that is not load-bearing does not block the gate.
For the benefit slot specifically, a claim about medication adherence benefit, refill timing, or appointment adherence that appears in the K/W layer passes the gate without a full evidence chain.
A claim about efficacy or clinical outcome that does not appear in K/W and is not common knowledge is a load-bearing gap and requires a campaign row before the draft may proceed.

**GAP**: the pack does not specify what counts as "common knowledge" in a healthcare SMS context.
Whether "refilling on time helps keep your levels steady" is common knowledge or requires a K/W entry is undecided.
This is a judgment the `_SCHEMA.md` expects the pack to resolve, and it does not.

### 4 · What desk-rejects an SMS

**Named rejection signals**: conditions the self-review checklist catches before release.

```text
  ❌ LENGTH       message exceeds 160 chars with no documented justification
                  for a second segment
  ❌ CTA          absent, or non-specific ("talk to your doctor")
  ❌ OPT-OUT      absent
  ❌ JARGON       clinical terms in a patient-audience body
  ❌ CLAIM        factual claim not tied to K/W or flagged as common knowledge
  ❌ VARIABLE     personalization variable not available in data pipeline
```

The checklist in `venue-sms/style-profile.md` adds two more flags that belong to the artifact's metadata state rather than to the text: `adopted_A` and `declined_A` must be present in the artifact frontmatter, and the tone must match the declared audience profile.

**GAP**: no stage in the current lifecycle programmatically reads the self-review checklist or validates the artifact frontmatter schema.
Both exist as prose in `style-profile.md`, but nothing enforces them at gate time.
The `_SCHEMA.md` implies a gate should apply these checks; the mechanism is absent.


## Aims

### A1 · Channel gates: what SMS enforces before any claim is asked
- A1.1 · The length, language, link, and opt-out constraints are checked before any artifact is released.
  **Done when:** a draft artifact passes through a gate that verifies the 160-character limit, the presence of one specific CTA, and the presence of an opt-out mechanism.

### A2 · The 4-slot template: how the 160 characters are divided
- A2.1 · The benefit slot's claim is traced to a K/W entry or flagged as common knowledge before draft.
  **Done when:** every benefit-slot sentence in a released artifact names its claim source.
- A2.2 · The audience axis (patient vs clinician) is declared in the artifact frontmatter and controls tone.
  **Done when:** every released artifact carries `audience: patient | clinician` in its frontmatter and the body matches the audience profile.

### A3 · Claims settlement: what "light" means for this channel
- A3.1 · The boundary between "common knowledge" and a K/W-required claim is settled for healthcare SMS.
  **Done when:** JL rules on what counts as common knowledge in this context and the ruling is recorded in Law.

### A4 · What desk-rejects an SMS
- A4.1 · The self-review checklist and artifact frontmatter schema are read by a stage gate, not left as prose.
  **Done when:** at least one stage gate programmatically checks the checklist items and the frontmatter fields named in `style-profile.md`.

### P · Page-level
- P1 · Every GAP item named in Content has either a ruling in Law or an open Decision Now row.
  **Done when:** the three GAP items (personalization fallback, common-knowledge boundary, checklist enforcement) are each addressed by a Law ruling or a Decision Now row.


## States

### Decision Now

- [ ] 🗣 What is "common knowledge" in a healthcare SMS context?
      📍 `Part 3` claims settlement §3 names this gap; it blocks A3.1.
      🔔 `Why now` the benefit slot must cite K/W or common knowledge, but the pack never defines the boundary, so every draft must guess.
      ⭐ `A ·` JL rules a short list of presumed-common-knowledge claim types for this channel (e.g. "refill timing affects adherence", "staying on schedule helps outcomes") — this list is recorded in Law and the claims stage reads it.
      `B ·` the gap stays open and every benefit-slot claim is required to have a K/W entry, removing common-knowledge as a path.
      → CC recommends A, because a ruled list is reusable across drafts and removes the per-draft guess without requiring a full K/W entry for claims that genuinely are common knowledge in this domain.
      🛑 `Blocks` A3.1 and P1.
      🤖 `If nobody answers` B takes effect: require K/W for every claim until JL rules otherwise.

- [ ] 🗣 What is the fallback when a personalization variable is missing?
      📍 `Part 2` §2.2 names this gap; it affects every patient-audience draft where medication or name data is absent.
      🔔 `Why now` a draft cannot be instantiated when a variable is absent and no fallback is specified; the pipeline either fails silently or produces a broken message.
      ⭐ `A ·` define a ranked fallback: (1) generic noun ("your medication"), (2) omit the slot token and compress, (3) block the artifact with a pipeline error.
      `B ·` treat any missing personalization variable as a blocking error: the artifact cannot be drafted until the variable is available.
      → CC recommends A, because a rigid block on missing medication name would stall patient-facing drafts in populations where medication name is not available in the pipeline, while a graceful fallback produces a usable (if less personalized) message.
      🛑 `Blocks` A2.2 and P1.
      🤖 `If nobody answers` B takes effect: treat missing variables as blocking errors.

### A1 · Channel gates: what SMS enforces before any claim is asked
- ⬜ A1.1 · Not started. No stage gate currently checks the 160-character limit or the opt-out field programmatically.

### A2 · The 4-slot template: how the 160 characters are divided
- ⬜ A2.1 · Not started. Claim sources are specified in the template but nothing enforces traceability at draft time.
- ⬜ A2.2 · Not started. The audience field is declared in the frontmatter schema but no gate validates it.

### A3 · Claims settlement: what "light" means for this channel
- 🧠 A3.1 · Waiting on JL to rule what counts as common knowledge for healthcare SMS (Decision Now above).

### A4 · What desk-rejects an SMS
- ⬜ A4.1 · Not started. The checklist and frontmatter schema live in `style-profile.md` as prose; nothing reads them at gate time.

### P · Page-level
- 🧠 P1 · Waiting on the two Decision Now rulings above before the three GAP items can be closed.


## Files

### Input files
- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/application/venue/venue-sms/README.md`
  Stage requirements block, 4-slot template, lifecycle mappings, and hard constraints; the primary source for §1, §2, and §3.
- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/application/venue/venue-sms/style-profile.md`
  Voice examples, drafting rules, audience pairing, self-review checklist, and artifact frontmatter schema; the primary source for §2.1, §2.2, and §4.
- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/application/venue/_SCHEMA.md`
  The schema every venue pack must answer; used to identify which gaps represent genuine missing answers vs. deliberate scope limits.

### Contracts
- `QBv1@paper` (`../../../PaperSkillBoard-260725/board.md`)
  Shape precedent for a venue pack page in this board family: desk-personality Opening, Content organized by what the venue gates, Aims and States mirroring Content divisions; adapted here with channel rather than journal desk as the organizing concept.


## Log

260802 · Opened. Three GAP items identified from _SCHEMA.md cross-check: personalization fallback rule, common-knowledge boundary, checklist enforcement mechanism. Two Decision Now rows written. All Aims ⬜ or 🧠 pending those rulings.
