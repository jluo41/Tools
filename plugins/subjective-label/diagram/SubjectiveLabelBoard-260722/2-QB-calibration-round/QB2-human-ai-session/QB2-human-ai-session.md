# Human-AI sessions: co-evolving labels and policy without anchoring
state: ✅ SETTLED
owner: JL
method: Six interaction groups preserve blind judgment, human authority, resumable dialogue, and a complete decision trace.

## Opening
What happens inside a Human-AI Session?
Blind first judgment, final labels, regions, reasons, and guideline edits must develop together without model anchoring.
A Session is one resumable conversation inside a Calibration Round.
Hidden pre-labels stay sealed until the human locks the batch's blind decisions.
This page settles the six interaction groups, human authority, resume state, and the trace that links each concept change to affected records.

**Where this page sits**: QA0 governs the revised conception, QB1 owns entry into the first Calibration Round, and QB3 owns the Checkpoint that closes a Round.

**Why it matters**: Showing model votes too early can bend the human judgment, while untracked dialogue can separate the final label from the reason and rule that produced it.

**What is settled**: The Session follows six groups in order and preserves every revision without allowing the agent to create human gold.

**Open settings**: Autosave cadence, resume-tail length, and the suggested item limit per Session remain numeric configuration values that pilot use may tune.

## Diagram
**The Session loop**: six groups move one resumable conversation from a sealed start to a checkpoint-ready trace.

```text
🔐 1 ENTER + RESUME
        │
        ▼
🙈 2 BLIND FIRST JUDGMENT
        │
        ▼
🤖 3 AGENT ELICITATION
        │
        ▼
🧑 4 HUMAN FINAL RECORD
        │
        ▼
📜 5 GUIDELINE + CONCEPT CHANGE
        │
        ▼
🧾 6 HISTORY + SESSION EXIT ──▶ 📌 QB3 CHECKPOINT
```

## Content

### 1 · Enter and resume
**The resumable session state**: one stable identity restores the round, batch, policy draft, conversation, and exact work cursor.

```text
🔁 ROUND t
  └──💬 SESSION s
      ├──🧑 human + 🤖 agent identity
      ├──📦 batch order + 📄 active item
      ├──📜 closed input + ✍️ current draft
      ├──🧾 event cursor + 💬 chat cursor
      └──🔒 sealed pre-label reference
```

The Session begins from one saved Round state and may resume after an interruption without changing its identity.

#### 1.1 · Required entry state
(Fixes the minimum state that makes the interaction reproducible and safe to resume.)
The entry record names the Round, Session, human, strong agent and version, ordered batch item identifiers, prior closed guideline, current draft guideline, and sealed pre-label record.
It also names the active item, completed items, unresolved items, pending guideline patches, latest event sequence, and latest chat sequence.
Round 1 records that no prior pre-labels or closed guideline exist rather than inventing empty predictions.

#### 1.2 · The six-group roster
(Makes the approved interaction order visible without turning it into six independent workflows.)
Group 1 enters or resumes the saved Session state.
Group 2 captures a blind first judgment before any machine prediction is visible.
Group 3 lets the agent elicit evidence, alternatives, and counterfactuals without taking authority.
Group 4 records the human's final class, region, rationale, and uncertainty state.
Group 5 versions guideline edits and flags clarification, correction, or concept revision.
Group 6 preserves chat and decision history and hands checkpoint-ready outputs to QB3.

#### 1.3 · Pause and resume behavior
(Keeps a temporary interruption from creating a second history or a reconstructed memory.)
Every human commit, label revision, guideline disposition, item transition, and pause writes the structured state before the interface moves on.
A resumed Session restores the last committed item state and then shows a generated summary beside the exact recent chat tail.
The agent must state when its version, available context, or restored artifact differs from the saved state.
An intentional end starts a new Session inside the same Round, while a disconnect or planned pause resumes the existing Session identifier.

#### 1.4 · Configurable numeric settings
(Keeps operational tuning visible without reopening the settled Session contract.)
`session.autosave_seconds` sets the backup cadence between event-triggered saves.
`session.resume_tail_messages` sets how many recent verbatim messages accompany the structured resume summary.
`session.suggested_item_limit` sets when the interface suggests a break or a new Session within the same Round.
Pilot evidence may change these values without changing the six-group roster or creating a blocking human decision.

### 2 · Blind first judgment
**The anchoring barrier**: the human sees the item and the accepted policy, while every machine outcome signal remains sealed.

```text
👁 VISIBLE                         🔒 SEALED
├──📄 item text                   ├──🧠 weak-model classes
├──📜 prior closed guideline      ├──📊 votes + confidence
├──🏷 H/L/N definitions           ├──🧾 model rationales
└──🗂 neutral source metadata     └──🗺 scorer region + pool source
                 │
                 ▼
          🧑 INITIAL COMMIT
```

Blind means independent of machine predictions and selection signals, not deprived of the project's accepted label definitions.

#### 2.1 · Visible and hidden information
(Defines the exact evidence boundary before the initial human commit.)
The human may see the item text, stable non-outcome metadata, label definitions, and the prior closed guideline.
The interface hides weak-model labels, votes, confidence, rationales, region scores, disagreement or consensus status, novelty status, and the item's sampling stratum.
The strong agent must not leak those fields through wording, ordering, hints, or summaries.

#### 2.2 · Initial human commit
(Creates an independent baseline before the dialogue starts changing the decision.)
The human records an initial H, L, or N class, confidence, and a brief evidence basis before the agent offers an interpretation.
A preliminary region may be recorded when it is already clear, but the final region remains open for dialogue.
The commit stores its time, item identifier, policy version, and visibility state.
The initial record is never overwritten by a later judgment.

#### 2.3 · Reveal gate
(Prevents one revealed committee result from influencing later blind decisions in the same batch.)
The sealed pre-label record remains hidden until the whole batch's blind human pass is locked.
Only then may the Session reveal model predictions for error diagnosis and guideline optimization.
Round 1 passes this gate by recording that no pre-label record exists.

### 3 · Agent elicitation
**The neutral elicitation path**: the agent turns one human judgment into explicit evidence, alternatives, and a transferable boundary test.

```text
🧑 initial class
      │
      ├──▶ 🔎 decisive evidence
      ├──▶ ⚖️ strongest alternative
      ├──▶ 🔁 smallest flip condition
      ├──▶ 🔗 comparison with prior human cases
      └──▶ 🚩 contradiction or missing rule
                    │
                    ▼
             🧾 rationale candidate
```

The agent elicits the human concept through questions and comparisons while keeping every proposed interpretation visibly provisional.

#### 3.1 · Question order
(Uses a stable neutral sequence so the agent does not steer the answer through selective prompts.)
The agent first asks which words, implications, or absences support the initial class.
It then asks which alternative class is strongest and why that alternative loses.
It asks for the smallest change that would flip the decision.
It may compare the item with earlier human-confirmed cases and point out a conflict between the current reason and an accepted rule.

#### 3.2 · Agent authority boundary
(Allows active assistance without turning an agent proposal into human gold.)
Before the initial commit, the agent may ask only neutral process questions and may not suggest a class, region, or rationale.
After the commit, it may propose contrasts, paraphrases, candidate regions, and guideline patches using visible human evidence and accepted policy text.
It must label each proposal as an agent proposal and preserve the human's own words beside any normalized version.
It cannot confirm the final item record, accept a semantic guideline patch, or clear a concept-change flag.

#### 3.3 · Revision during dialogue
(Lets labels and reasons improve while preserving how and why they changed.)
The human may revise the initial class, region, confidence, or rationale after elicitation.
Each revision records the before value, after value, actor, reason, policy version, and source event.
The human classifies the revision as clarification, concept revision, or correction of a momentary mistake.
The current display shows the latest values, while the decision trace keeps every earlier value.

### 4 · Human final record
**The human-owned item result**: one explicit confirmation binds the final class, diagnostic region, rationale, uncertainty, and revision status.

```text
🧑 HUMAN CONFIRMATION
├──🏷 final class       H | L | N
├──🗺 final region      H | L | N | HL | LN | HN | HLN
├──🧾 final rationale  evidence + rejected alternative
├──🔁 flip condition   smallest decision-changing change
├──🌡 uncertainty      confidence + reason + review state
└──🚩 revision kind    none | clarification | correction | concept revision
```

The final record keeps class, region, and uncertainty separate because they answer different questions.

#### 4.1 · Final item schema
(Defines the complete record that becomes human-confirmed data at the Round Checkpoint.)
The human confirms one final class, one final diagnostic region, decisive evidence, the strongest rejected alternative, a counterfactual flip condition, confidence, and an uncertainty reason.
The record also stores the raw human rationale, any human-accepted normalized rationale, and the policy version active at confirmation.
NONE means insufficient trait evidence and never stands in for uncertainty.
An item that cannot be resolved receives an explicit unresolved state rather than a forced class disguised as consensus.

#### 4.2 · Final authority
(Makes the confirmation event the only route from dialogue to human gold.)
The agent may prepare the record, but the human confirms or edits every semantic field.
Only an explicit human confirmation marks the item checkpoint-ready.
Chat text may show what the human said, but the structured confirmation event is the authoritative record used downstream.

#### 4.3 · Post-reveal reconsideration
(Allows human correction after model comparison without hiding the new anchoring risk.)
After the batch blind pass locks, sealed pre-labels may be revealed and compared with the human records.
If the human changes an item after that reveal, the system appends a new revision with `post_reveal: true` and preserves the pre-reveal decision.
A post-reveal semantic change enters blind re-review at the Checkpoint before it can replace the earlier human record.

### 5 · Guideline and concept change
**The co-evolution record**: each accepted lesson changes a versioned draft and declares whether the human concept itself moved.

```text
📄 item decision + 🧾 reason
            │
            ▼
🤖 patch proposal
├──✏️ editorial
├──💡 clarification
└──🚩 concept revision
            │
            ▼
🧑 accept | reject | reframe
            │
            ▼
📜 current draft + 🔁 impact queue
```

Guideline edits may develop item by item, but no edit silently rewrites the construct or the evidence that came before it.

#### 5.1 · Patch record
(Links every proposed rule change to the item and reasoning that raised it.)
A patch records its trigger item, old text, proposed text, rule scope, supporting rationale, counterexample, affected labels or regions, proposer, and human disposition.
The human may accept, reject, or reframe an agent patch.
An accepted patch enters the current draft guideline with a new immutable version identifier.
Rejected and reframed proposals remain in the trace so the same failed suggestion is not rediscovered without context.

#### 5.2 · Concept-change classification
(Separates clearer wording from a real movement of the semantic boundary.)
An editorial edit changes expression or formatting without changing a decision rule.
A clarification makes an intended boundary explicit and may trigger targeted regression checks.
A correction repairs a mistaken item application without changing the intended concept.
A concept revision changes what the human means by H, L, or N and sets `concept_change: true`.

#### 5.3 · Backward impact
(Protects earlier labels and rules when the semantic authority changes the construct.)
Every concept revision names the affected rule, classes, regions, prior guideline versions, and candidate earlier items.
Those items enter a backward review queue and cannot be silently relabeled by the agent.
Later items record the exact draft policy version they encountered, while sealed pre-labels remain tied to the prior closed guideline.
QB3 decides which reviewed changes freeze into the next closed guideline and cumulative gold version.

### 6 · History and session exit
**The durable trace**: an append-only event stream preserves the conversation, decisions, versions, visibility gates, and checkpoint handoff.

```text
💬 CHAT EVENTS ───────┐
🏷 ITEM REVISIONS ────┤
📜 POLICY PATCHES ────┼──▶ 🧾 DECISION TRACE
🚩 CONCEPT FLAGS ─────┤         │
🔐 VISIBILITY EVENTS ─┘         ▼
                         ⏸ pause | ✅ end | 📌 checkpoint-ready
```

Chat history preserves the conversation, while the decision trace makes its consequential results directly inspectable.

#### 6.1 · Append-only history
(Ensures that resume and audit use recorded events rather than regenerated memory.)
Every event stores a sequence number, timestamp, actor, Round, Session, item, event type, visibility state, and referenced artifact versions.
Human messages, agent messages, interface actions, item revisions, guideline dispositions, and reveal events remain in order.
Corrections append new events and never replace the original event.

#### 6.2 · Decision trace
(Connects each current result to the human words, agent proposal, and policy state that produced it.)
The trace links the initial judgment, all revisions, final confirmation, region history, rationale history, guideline patches, concept-change flags, and checkpoint disposition for each item.
It distinguishes verbatim human text from agent summaries and normalized rationales.
A reader can reconstruct what changed, who changed it, what information was visible, and which policy version governed the decision.

#### 6.3 · Session exit states
(Stops a conversation cleanly without letting the Session close the Calibration Round.)
A paused Session saves its cursor and waits for resume under the same Session identifier.
An ended Session emits completed items, unresolved items, pending and accepted patches, concept-change impacts, and the final event cursor.
A checkpoint-ready Session has no unsaved human decisions and names every unresolved item or policy question explicitly.
Only QB3's Checkpoint may freeze the Round's human gold, cumulative gold, and next closed guideline.

## Aims

### A1 · 🔐 Enter and resume
- A1.1 · A Session can restore the exact round, batch, policy, item, and conversation state after interruption.
  **Done when:** Section 1 names one stable Session identity, the required saved fields, pause behavior, and non-blocking numeric configuration.

### A2 · 🙈 Blind first judgment
- A2.1 · Every initial human judgment is independent of weak-model predictions and selection signals.
  **Done when:** Section 2 defines the visible fields, sealed fields, initial commit, and batch-level reveal gate.

### A3 · 🤖 Agent elicitation
- A3.1 · The agent elicits transferable reasons without taking semantic authority or leaking sealed evidence.
  **Done when:** Section 3 fixes the neutral question order, proposal boundary, and versioned revision behavior.

### A4 · 🧑 Human final record
- A4.1 · Every completed item has one explicit human-confirmed class, region, rationale, and uncertainty record.
  **Done when:** Section 4 defines the final schema, human confirmation event, unresolved path, and post-reveal protection.

### A5 · 📜 Guideline and concept change
- A5.1 · Every guideline patch and concept revision is versioned, given a human disposition, and linked to backward impact.
  **Done when:** Section 5 separates editorial edits, clarifications, corrections, and concept revisions and routes affected earlier items to review.

### A6 · 🧾 History and session exit
- A6.1 · Chat history and the structured decision trace can reconstruct every consequential Session change.
  **Done when:** Section 6 links actors, visibility, item revisions, guideline versions, and concept flags in append-only order.
- A6.2 · A Session can pause, end, or become checkpoint-ready without closing its Calibration Round.
  **Done when:** Section 6 defines all three exit states and leaves freezing authority with QB3.

## States

### A1 · 🔐 Enter and resume
- ✅ A1.1 · Met; Section 1 fixes stable identity, full resume state, interruption behavior, and configurable numeric settings.

### A2 · 🙈 Blind first judgment
- ✅ A2.1 · Met; Section 2 keeps all model and selector outcome signals sealed through the batch's blind human pass.

### A3 · 🤖 Agent elicitation
- ✅ A3.1 · Met; Section 3 gives the agent a neutral elicitation sequence and no authority to create final human records.

### A4 · 🧑 Human final record
- ✅ A4.1 · Met; Section 4 gives each item an explicit human confirmation, separated class, region, uncertainty, and protected post-reveal revision path.

### A5 · 📜 Guideline and concept change
- ✅ A5.1 · Met; Section 5 versions every patch, records the human disposition, flags concept revision, and creates backward impact review.

### A6 · 🧾 History and session exit
- ✅ A6.1 · Met; Section 6 preserves append-only chat and structured decision events with actors, versions, and visibility state.
- ✅ A6.2 · Met; Section 6 defines pause, end, and checkpoint-ready exits while QB3 retains Round closure authority.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 §5](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Keep the human as semantic authority while models retrieve, elicit, diagnose, and draft.
- `constrained by · ALL` · [QA0 §12](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Keep the Session inside one Calibration Round and leave closure to the Checkpoint.
- `continues · ALL` · [QA0 §14](1-QA-semantic-contract/QA0-the-revised-conception/QA0-the-revised-conception.md)
  Realize the governing human-first interaction loop as a resumable six-group Session contract.

## Law
- 260806 JL · 🙈 Human judgment moves first and every later influence remains traceable
      The Session seals machine outcomes until the batch's blind human pass is locked, gives the human final semantic authority, and records every later label, rationale, region, and guideline revision as an append-only event.
      Revealing pre-labels before blind completion and allowing the agent to close semantic decisions were rejected because they create anchoring and transfer authority away from the identified human.

## Glossary
- 🔁 **Calibration Round**: one method cycle from a prior closed state through candidate preparation, pre-labeling, Human-AI Sessions, and Checkpoint closure.
- 💬 **Human-AI Session**: one continuous or resumed conversation between the human semantic authority and strong labeling agent inside a Calibration Round.
- 🙈 **Blind first judgment**: the human's initial class and reason recorded before any weak-model prediction, vote, confidence, rationale, region score, or selection signal is visible.
- 🧾 **Decision trace**: the structured, append-only links among chat events, item revisions, policy versions, visibility gates, and human confirmations.
- 🚩 **Concept revision**: a human-confirmed change to what H, L, or N means that requires backward impact review.
- 📌 **Checkpoint**: the QB3 closure event that freezes the Round's human gold, cumulative data, metrics, and closed guideline version.

## Log
260806 · This DRAFT round replaced the previous-edition three-layer evaluation purpose with the approved Human-AI Session contract and six-group roster.
