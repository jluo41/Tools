# Delivery Design: advice the tail adopts or declines

state: 🔴 OPEN
owner: JL

## Opening

What does rung 1d-advice deliver, and how does an advice entry bind a downstream stage without becoming a requirement it cannot escape?

Rung 1d is the top of the venue-FREE evidence ladder (descriptions -> themes -> claims -> advice) and is the ladder's deliverable rung: it translates the claim ledger into guidance an artifact stage can act on.
Each entry (A1, A2, ...) carries one of three roles: exploit (settled evidence), explore (a deliberate test-to-learn bet), or negative advice (derived from a refuted claim).
The entry's derivation chain (A<-C traceability) is mandatory; an entry without a backing claim is not advice, it is vibes, and the ladder exists to prevent exactly that.
Downstream venue-ALIGNED stages (pitch, narrative, display, artifact) adopt or decline each entry per their own venue and audience, and a declined entry waits for the next round rather than being discarded.
This page owns what that delivery looks like and what rules keep the adopt/decline decision honest.

**Covered elsewhere**: QB2@paper (QB2 on the paper board) holds the narrative arc that is built from the claim ledger once advice has been produced; here the question is what 1d-advice puts on the table for that arc to consume.
QB4 Value and QB3 Literature on the paper board describe returned evidence; this page asks how that evidence is converted into actionable guidance before it enters the arc.

**Why the adopt/decline split matters**: it is what keeps rung 1d venue-FREE.
If the advice stage decided which entries apply, it would have to know the modality, the audience, and the channel rules before writing the first entry.
Instead, 1d writes all guidance the evidence supports; the venue-ALIGNED stages then select, each recording which A<n> it takes and which it leaves, with a one-line reason.
The record lives downstream, the ladder doc stays clean, and a retarget to a new venue starts with the same advice table rather than a new derivation.

**The naming echo**: JL renamed "principles" to "advice" on 2026-07-09 because counsel is falsifiable by adoption in a way that a principle is not.
An adopted entry either produces a message move the artifact can execute or it does not; a principle can always be argued to apply.
The word "advice" also acknowledges the DIKW analogy: rung 1d is the wisdom rung of the evidence ladder, and wisdom that cannot be tested is not wisdom.


## Diagram

**Advice as the ladder's deliverable**: where 1d sits, how entries flow downstream, and the adopt/decline gate.

```text
  venue-FREE evidence ladder
  ──────────────────────────
  1a descriptions   what the data looks like
  1b themes         what patterns emerge
  1c claims         what generalizes (the ledger)
  1d advice         what the evidence advises  ← DELIVERABLE
        │
        │  A<n> entries, each: role + derivation + status
        │
        ▼
  venue-ALIGNED downstream stages
  ────────────────────────────────
  2-pitch           ADOPT or DECLINE per venue + audience
  3-narrative       ADOPT or DECLINE
  4-display         ADOPT or DECLINE
  5-artifact        ADOPT or DECLINE

  🔑 an adopted A<n> traces: artifact ─▶ A<n> ─▶ C<n> ─▶ anchor
  🚫 declined entries stay in 1d-advice for the next round
  🚫 1d is content-WHAT; venue Artifact Principles are channel-HOW
```


## Content

### 1 · The advice entry and its three roles

**What an advice entry carries**: the three roles, the derivation requirement, and the actionability test.

```text
  📋 ONE ADVICE ENTRY
  ───────────────────
  id         A<n>  (ladder-local; traces downstream)
  role       exploit | explore | negative advice
  derivation >= 1 C<n> from the 1c ledger (mandatory)
  status     active | declined | rejected
  scope      boundary and caveat when derivation is weak

  🔑 actionability test: "could the artifact stage write
     the exact message move from this line?"
  🚫 fail = claim restated, push back to 1c
```

📌 An advice entry is not a claim rephrased; it is a guidance sentence that an artifact stage can execute without re-deriving the evidence.

The exploit role applies when the backing claims are settled: the entry acts on known evidence and fails the CHECK gate if the venue's settlement bar is not met.
Negative advice is also exploit-role, because a refuted claim is settled evidence; the entry says "avoid X" and the refutation is the derivation.
The explore role is a deliberate bet: a weak or gap claim may back it, but three conditions must be visible in the entry itself to pass CHECK (the explore tag, the settling claim named as `Settles: C<n> via iterate`, and the compliance rails).
A missing tag or a missing settling claim makes an explore entry indistinguishable from an ungrounded one, which is why CHECK enforces all three conditions rather than trusting the author's intent.

#### 1.1 · Derivation is what separates advice from opinion
(an entry without a C<n> in its derivation is a recommendation the ladder cannot defend)
The claim ledger is the authority, and every entry must point at it.
When a DRAFT entry cannot name a backing claim, it either surfaces a gap (which routes back to 1c as a question section) or it does not belong in the advice document at all.

#### 1.2 · The actionability test is the second gate
(passing derivation but failing actionability means the entry is still a claim in disguise)
The test is one concrete question: could the artifact stage write the exact message move from this line?
An entry that answers "probably, with some interpretation" has not passed.
The revision phase exists precisely to sharpen entries that pass derivation but fail this test.

### 2 · Adopt, decline, and what each commits downstream to

**The adopt/decline mechanism**: how a venue-ALIGNED stage takes or leaves an entry, and what the record says.

```text
  1d-advice.md (venue-FREE)
  ─────────────────────────
  A1  exploit  active     ← downstream may ADOPT or DECLINE
  A2  explore  active
  A3  negative active

        │ADOPT                    │DECLINE
        ▼                         ▼
  entry executes              entry stays in 1d
  in the artifact             for the next round
  record lives DOWNSTREAM     reason is recorded downstream
  traces: artifact→A→C→anchor no edit to 1d-advice.md
```

📌 The adopt/decline split is what allows the same advice table to serve multiple venues without being rewritten.

A declined entry is not a failure; it is a design choice that the venue or audience makes explicit.
An entry declined by a short-message venue may be adopted by a dashboard venue that can afford the space; keeping it in the 1d document is what makes that possible.
The downstream record (which A<n> was adopted, which declined, and the one-line why) is the traceability the claim-audit later follows: artifact -> adopted A -> C -> anchor.
If an adopted entry has no record, the audit cannot verify it was grounded.

#### 2.1 · Declined entries stay in 1d, which is why 1d is not a per-venue document
(rewriting 1d per venue would lose every entry that did not fit the first venue)
The venue-FREE property is not a formatting choice; it is the condition that makes the advice table reusable across rounds and modalities.
An entry the current venue declines may become load-bearing when the venue changes.

#### 2.2 · The record living downstream keeps 1d clean
(if adoption records lived in 1d, the document would accumulate venue-specific annotations that do not belong on a venue-FREE rung)
The downstream stage owns its adoption record.
The 1d document knows only whether an entry is active, rejected after consideration, or consumed by an adoption.

### 3 · How advice binds to narrative without becoming mandate

**The content-WHAT / channel-HOW boundary**: what advice governs and what it leaves to the venue stage.

```text
  content-WHAT (this page)          channel-HOW (venue Artifact Principles)
  ─────────────────────────         ─────────────────────────────────────────
  what the message should do        length, cadence, format
  which claim it executes           the arc shape for this modality
  the evidence warrant              tone-by-audience rules
  venue-FREE, survives retarget     venue-ALIGNED, rewritten on retarget

  🔑 narrative (QB2@paper analog) reads BOTH
  🚫 the two documents never merge
```

📌 Advice says what the content must accomplish; the venue says how to accomplish it in the given channel.

The narrative stage (haipipe-application-narrative, stage 3) reads 1d-advice for what to compose and reads 2-venue for how to compose it.
A beat in the narrative is anchored to an A<n> (or the C<n> it derives from), which is what keeps the arc honest; a beat with no anchor is copy, not narrative.
The advice document makes no claim about length, register, or section order, because those decisions are venue-specific and get rewritten on retarget.
The parallel to QB2@paper is direct: paper's Work page owns the arc that is built from the claim ledger, and application's 1d-advice is the ledger-level upstream that the narrative consumes.

#### 3.1 · The naming history is load-bearing context
(JL's 2026-07-09 rename from "principles" to "advice" changed what downstream stages are allowed to do)
A principle that a venue declines requires an argument for why the principle does not apply.
Advice that a venue declines requires only a one-line design reason.
The rename shifted the burden of justification from the stage that declines to nobody: declining is a legitimate choice, and the entry waits rather than disappearing.

#### 3.2 · Explore advice is the mechanism for learning through deployment
(an explore entry deploys a bet, and the A/B result flows back to the claim ledger)
When an explore entry is adopted and deployed, the arm result routes back to 1a descriptions, flows through the ladder, and either flips the backing claim to supported (graduating the entry to exploit) or adds it to the Rejected reservoir.
This is not a workaround for weak evidence; it is the designed path for turning a bet into settled knowledge.
The visible tag and the named settling claim are what make the bet legible rather than invisible.


## Aims

### Decision Now

- [ ] 🗣 Should the sweep-or-waive lens be stated as the CHECK gate for the triple (exploit / explore / negative), or does that belong in the haipipe-application-advice SKILL.md?
      📍 `Part 1` · which document owns the gate wording for the three roles
      🔔 The assignment names the sweep-or-waive lens as exactly the triple; settling whether this page or the SKILL carries it avoids duplication.
      ⭐ `A · State it here as a cross-reference`: name the triple and point to SKILL.md for the gate mechanics; this page owns the design rationale, the SKILL owns the execution contract.
      `B · Keep it in SKILL.md only`: this page describes but does not restate the gate; simpler, but a reader of this page has to follow the link to see whether their entry qualifies.
      → JL recommends A, because the rationale for why the triple exists belongs beside the Content that explains the roles, while the gate mechanics belong in the executable SKILL.
      🛑 Blocks nothing on this page; the Content already names all three roles.
      🤖 If nobody answers: treat as A (cross-reference without restating gate mechanics).


### A1 · The advice entry and its three roles

- ⬜ A1.1 · Every active advice entry carries a derivation chain to at least one 1c claim.
  **Done when:** no active A<n> in a 1d-advice.md file lacks a C<n> citation in its derivation field.
  **Now:** Not started; no live 1d-advice.md file has been checked for derivation completeness.
- ⬜ A1.2 · The explore role carries all three contract conditions (tag, settling claim, rails).
  **Done when:** CHECK rejects an explore entry that is missing any one of the three, on any venue tier.
  **Now:** Not started; CHECK behavior for explore entries has not been verified on a real file.
- ⬜ A1.3 · The actionability test is applied before an entry reaches CHECK.
  **Done when:** the revision phase includes an explicit actionability pass, and entries that fail it are pushed back to 1c rather than caveated inline.
  **Now:** Not started; whether the revision phase enforces an actionability pass is not confirmed from a live run.


### A2 · Adopt, decline, and what each commits downstream to

- ⬜ A2.1 · Declined entries remain in the 1d document and are readable in the next round.
  **Done when:** a venue retarget finds the prior round's declined entries available in 1d-advice.md without any gap.
  **Now:** Not started; no retarget has been observed with a prior round's declined entries available.
- ⬜ A2.2 · The adoption record living downstream is sufficient for claim-audit to trace artifact -> A -> C -> anchor.
  **Done when:** a claim-audit run on an advice-adopting artifact finds the A<n> record in the downstream stage without reading 1d-advice.md.
  **Now:** Not started; no claim-audit run has been traced back through an adopted A<n>.


### A3 · How advice binds to narrative without becoming mandate

- ⬜ A3.1 · Narrative beats are anchored to A<n> or C<n> ids, never to paraphrase.
  **Done when:** a narrative page produced from a 1d table has no beat lacking an explicit A<n> or C<n> anchor.
  **Now:** Not started; no narrative page produced from a 1d table has been inspected for beat anchoring.
- ⬜ A3.2 · The content-WHAT / channel-HOW boundary is stable across venue changes.
  **Done when:** a retarget to a new venue rewrites 2-venue.md without editing 1d-advice.md, and narrative beats re-anchor to the same A<n> ids.
  **Now:** Not started; no retarget test has been run.


### P · Page-level

- ⬜ P1 · A cold reader can distinguish advice (content-WHAT) from Artifact Principles (channel-HOW) after reading this page.
  **Done when:** a zero-background reviewer names the distinction correctly without reading haipipe-application-advice SKILL.md.
  **Now:** Not started; no zero-background review has been done.




## Files

### Contracts

- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/application/_old/1-lifecycle/1d-advice/haipipe-application-advice/SKILL.md`
  The executable spec for rung 1d: the four phases, the artifact skeleton, settlement coupling, and the CHECK gate for all three entry roles.

### Input files

- `/Users/jluo/Desktop/drfirst-ai-space/Tools/plugins/haipipe-toolkit/skills/application/_old/1-lifecycle/3-narrative/haipipe-application-narrative/SKILL.md`
  Stage 3 of the application lifecycle; shows how narrative reads both 1d-advice (content-WHAT) and 2-venue Artifact Principles (channel-HOW) when composing beats.
- `../../../PaperSkillBoard-260725/board.md`
  Cited as QB2@paper; paper's Work page owns the narrative arc built from the claim ledger, and this page's §3 establishes the application analog.


## Glossary

- **Exploit entry**: an advice entry backed by settled claims; subject to the venue's settlement bar at CHECK.
- **Explore entry**: an advice entry that is a deliberate test-to-learn bet; exempt from the settlement bar only when the explore tag, settling claim, and compliance rails are all present.
- **Negative advice**: an exploit-role entry derived from a refuted claim, saying what the artifact should avoid; the refutation is the derivation.
- **A<-C traceability**: the requirement that every A<n> entry names at least one C<n> claim as its derivation, so the claim-audit can follow the chain from artifact to evidence anchor.
- **Sweep-or-waive**: the CHECK lens applied to the three roles; an entry either meets the gate for its role or the gate is explicitly waived with a recorded reason.
- **Content-WHAT**: what the message should accomplish, owned by rung 1d; venue-FREE and survives retarget.
- **Channel-HOW**: how the message accomplishes it (length, cadence, format), owned by the venue's Artifact Principles; venue-ALIGNED and rewritten on retarget.


## Log

260802 · QB5-design.md created; Opening, Content (3 divisions), Aims, States, Files, and Glossary written from haipipe-application-advice SKILL.md, haipipe-application-narrative SKILL.md, and QB2@paper (QB2-work.md on the paper board). Decision Now row placed for the sweep-or-waive gate location.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0