# Delivery Deploy: gate, audit, and ship

state: 🔴 OPEN
owner: JL
method: mirror the paper's generate-then-promote asymmetry: audits raise a draft to reviewed, and only a person makes it deployed

## Opening
What must happen between a drafted artifact and a live intervention, and who may say go?
A drafted artifact is one message variant in `0-artifacts/`, such as an SMS text, with status draft.
A live intervention is that same variant sent to real patients through a channel.
Three moves sit between them: review, claim audit, and deploy, and the last is still a stub.
This page states what each move owes and keeps one rule: nothing self-promotes.

**What each move is**: the three moves as their skills define them today.
Review is the per-artifact compliance pass; it writes one `REVIEW-<variant-slug>.md` with a verdict of pass, revise, or fail.
Claim audit is the trace pass; it writes `0-artifacts/CLAIM_AUDIT.md` and walks every factual statement back through artifact to adopted A to C to anchor, the 1c ledger's chain.
Deploy packages a reviewed artifact for its channel; its SKILL.md is an explicit stub whose risk profile already forbids auto-deploy.

**Where this page sits**: drafting the artifact is upstream work and not this page's concern; this page begins when a variant exists in `0-artifacts/`.
QB9@paper is the precedent on the paper board: candidates a human reviews before anything becomes the submission, and this page carries that same asymmetry into the application family.

**Why it matters**: a wrong draft costs an edit; a wrong send reaches real patients on a live channel and cannot be unsent.
The deploy skill rates itself HIGH risk for exactly this reason, and every rule on this page exists to keep that risk behind a person.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**The skills are quoted, never improved**: Content states what review, claim-audit, and deploy do today, from their SKILL.md files.
The gap between today and a proposal is written as a gap with a Decision Now row, never as current behavior.

**Reviewed and deployed stay two words**: a machine may raise an artifact to reviewed, and only a person makes it deployed.
Never write a sentence in which one status implies the other.

**The stub stays named a stub**: deploy's seven steps are planned, not running.
Writing them in the present tense invites someone to trust a path that does not exist.

## Diagram
**From draft to live and back**: the three moves, the one human line, and the loop.

```text
  📄 draft ──▶ 🔍 review ──▶ 🧾 claim audit ──▶ ✅ reviewed
                                                    │
                              👤 a person says go · never auto-deploy
                                                    ▼
                  📤 deployed ── SMS · dashboard · email · in-app
                                                    │
                              📊 A/B results · deploy is itself a probe
                                                    ▼
                  🪜 1a-descriptions ── the next round's data
```

## Content

### 1 · The two audit passes
**Two passes over one artifact**: what each reads, what each writes.

```text
  📄 0-artifacts/<variant>.md · status: draft
        │
        ▼
  🔍 REVIEW · one report per artifact
     📥 reads     venue style-profile · 1d-advice · 1c-claims · 4-display
     📤 writes    0-artifacts/REVIEW-<variant-slug>.md
     ⚖️ verdict   pass | revise | fail
        │
        ▼
  🧾 CLAIM AUDIT · one report per artifact set
     🔗 trace     artifact → adopted A → C → anchor
     📤 writes    0-artifacts/CLAIM_AUDIT.md
     🚨 findings  orphan · overclaim · stale citation · missing citation
        │
        ▼
  ✅ frontmatter flips · draft → reviewed · only on a pass
```
🔍 Establishes what the two audit passes catch today, quoted from their skills, and what a pass is allowed to change on disk.

#### 1.1 · Review judges the artifact for its audience
(the checklist is compliance and safety, not prose taste)
The review skill runs a nine-row checklist per artifact.
The rows cover audience tone and length, claim traceability to adopted A ids, no refuted C or [STALE]-tagged A cited as settled, citation format per audience, element specs from 4-display and the venue style-profile, no PHI or PII or code or raw data values, a clear call to action, reading level, and a correct status field.
It writes one `REVIEW-<variant-slug>.md` into `0-artifacts/` with a verdict of pass, revise, or fail.
On a pass it flips the artifact's frontmatter from draft to reviewed, and that flip is the only write it makes outside its own reports.

#### 1.2 · Claim audit walks every statement back to its anchor
(a break anywhere in artifact → adopted A → C → anchor is a finding)
The claim audit reads 1d-advice, the 1c claim ledger, and every drafted artifact.
It traces each factual statement to the A entry it executes, on to the C claim that A derives from, and on to that claim's anchor.
Four failure kinds are findings: orphan claims absent from the ledger, overclaims stated more strongly than their evidence, stale citations to superseded entries, and factual statements with no backing at all.
A statement may cite a supported or a weak claim, never a GAP, and a weak claim forces a qualified sentence.
Scope creep is the audit's sharpest catch; the skill's own example is an artifact widening "in high-variability patients" to "all patients".
Its one write is `0-artifacts/CLAIM_AUDIT.md`; it never edits an artifact.

### 2 · The gate: nothing self-promotes
**The line only a person crosses**: two statuses, and the gap between them.

```text
  ✅ status: reviewed ── the machines' ceiling
        │
        │  👤 explicit human approval · never auto-deploy
        ▼
  📤 status: deployed ── SMS · dashboard · email · in-app

  🚫 forbidden   any code path that flips reviewed → deployed alone
```
🚪 Fixes the one act only a person may perform, mirrored from the paper board's promotion gate.

#### 2.1 · Reviewed is a ceiling, not a launch
Review and claim audit can together raise an artifact to reviewed, and that is as far as any machine may take it.
The deploy skill's risk profile is explicit: HIGH, deploys to external channels, must be gated by review plus explicit user approval, never auto-deploy.
QB9@paper fixed the same asymmetry for the paper: a human reviews a gate-passing candidate, and an explicit PROMOTE is the only way the candidate becomes the submission.
Here the two words are reviewed and deployed instead of candidate and promotion, and the property is identical: nothing self-promotes.

#### 2.2 · Staging first, approval in between
(the stub's planned step order already encodes the gate; implementation must not lose it)
The stub's planned steps verify prerequisites, package the artifact for its channel, deploy to staging, verify with a test send or preview render, and reach production only on approval.
The skills say a user must approve; none of them names which person that is, so the question sits in this page's Decision Now.

### 3 · Deploy ships, then feeds the ladder
**Deploy is itself a probe**: the ship step produces the next round's data.

```text
  📤 deployed variant ── live on its channel
        │
        │  📊 A/B results · delivery receipts · engagement
        ▼
  🪜 1a-descriptions ── new rows of described data
        │
        ▼
  🧵 1b themes → 1c claims → 1d advice → the next artifact
```
🔁 Places deploy inside the lifecycle loop rather than at its end.

#### 3.1 · Ship is not the finish line
A deployed variant is an experiment running on real recipients, and its A/B results flow back into 1a as newly described data.
That makes deploy a probe in the lifecycle's own sense: the artifact asks a question of its audience, and the channel returns the answer.
The stub already points this way: its last planned step logs the deployment in STATUS.md, so the round record survives the ship.

#### 3.2 · Implementing the stub is the open build
The deploy SKILL.md is an explicit stub at version 0.1.1: seven planned steps, four future channels (SMS vendor API, dashboard endpoint via /haipipe-end, email template system, in-app UI component), and no code.
Whatever implements it inherits part 2's gate whole; a convenient auto-ship flag would delete the one safety property this page exists to keep.

### 4 · The bucket shape: one proposal for 3-deliver
**Flat today, paper's shape tomorrow**: where the four skills would live.

```text
  📁 application/_old/3-deliver/ · today, flat
     haipipe-application-artifact · review · claim-audit · deploy

  📁 application/_old/3-deliver/ · proposed, mirroring paper
     1-build/  ── haipipe-application-artifact
     2-audit/  ── haipipe-application-review · claim-audit
     4-ship/   ── haipipe-application-deploy

  📁 paper/3-deliver/ · the precedent layout
     1-build/ · 2-audit/ · 3-polish/ · 4-ship/ · haipipe-paper-deliver
```
📁 Carries the context for the first Decision Now row; the ruling is JL's.

#### 4.1 · Why mirror the paper
The paper family already delivers from numbered buckets: `paper/3-deliver/` holds 1-build, 2-audit, 3-polish, and 4-ship, with `haipipe-paper-deliver` as the flat orchestrator beside them.
The application's four deliver skills sit flat today, and the proposal moves artifact to 1-build, review and claim-audit to 2-audit, and deploy to 4-ship.
The number 3 stays empty because nothing in the application family polishes yet, and an empty bucket is not created for symmetry.
The move is cheapest now: deploy is a stub, so no implementation path has hardened against the flat layout.

## Aims

### Decision Now
- [ ] 🗣 Do we re-bucket application/3-deliver into paper's layout?
      📍 `Part 4` the flat layout is today's fact; the mapping is artifact to 1-build, review and claim-audit to 2-audit, deploy to 4-ship
      🔔 `Why now` deploy is still a stub, so the move is a folder rename today and grows dearer once implementation hardens paths
      ⭐ `A ·` adopt the paper shape now: four folders move, every path pointing at them updates once, and the two deliver families read the same way; CC recommends A because the move is cheapest before the stub is implemented
      `B ·` keep the flat layout until deploy is implemented: no churn now, and the move rides along with the implementation change
      🛑 `Blocks` nothing; the skills run from the flat layout today
      🤖 `If nobody answers` B: the flat layout stays

- [ ] 🗣 Who may say go for a production deploy?
      📍 `Part 2` the deploy skill requires explicit user approval and never names the approver
      🔔 `Why now` the gate cannot be enforced in code until the approver is a named role
      ⭐ `A ·` JL approves every production deploy personally: slowest, and the safest while sends reach real patients; CC recommends A until one full deploy has run cleanly
      `B ·` the intervention's owner approves and JL is informed: scales past one person, and moves the approval one step away from the board's decider
      🛑 `Blocks` the first production deploy, and A2.1


### A1 · 🔍 The two audit passes
- ⬜ A1.1 · Every reviewed artifact carries both reports.
  **Done when:** each artifact whose frontmatter reads reviewed has a `REVIEW-<variant-slug>.md` with a pass verdict and appears in `CLAIM_AUDIT.md` with no open finding.
  **Now:** Not started here; the two skills exist as contracts (review 0.1.1, claim-audit 0.1.2) and no run report is cited on this page yet.


### A2 · 🚪 The gate: nothing self-promotes
- 🧠 A2.1 · A named person owns the production approval.
  **Done when:** JL answers the second Decision Now row and the ruling is written into the deploy skill's prerequisites.
  **Now:** Waiting on JL; the second Decision Now row above carries the options.
- ⬜ A2.2 · No code path flips reviewed to deployed on its own.
  **Done when:** the implemented deploy skill refuses production without a recorded approval, and one test run proves the refusal.
  **Now:** Not started; there is no code path to refuse anything while deploy is a stub.


### A3 · 🔁 Deploy ships, then feeds the ladder
- ⬜ A3.1 · Deploy is implemented past the stub.
  **Done when:** one artifact is packaged and delivered to a staging or test channel through the implemented skill, with a verified test send.
  **Now:** Not started; the deploy SKILL.md declares itself STUB at 0.1.1.
- ⬜ A3.2 · A shipped variant's results land back in 1a.
  **Done when:** one deployment's A/B results are written into 1a-descriptions and the next round's themes can cite them.
  **Now:** Not started; nothing has shipped, so nothing has flowed back.


### A4 · 📁 The bucket shape: one proposal for 3-deliver
- 🧠 A4.1 · The 3-deliver folder shape is ruled, one way or the other.
  **Done when:** the first Decision Now row is answered and the folder layout matches the ruling.
  **Now:** Waiting on JL; the first Decision Now row above carries the options.


## Files

⚙️ **Engines** · what RUNS the subject

- `../../../../application/_old/3-deliver/haipipe-application-review/SKILL.md`
  The review pass; open it to change the checklist or the verdict rules.
- `../../../../application/_old/3-deliver/haipipe-application-claim-audit/SKILL.md`
  The trace pass; open it to change what counts as a finding.
- `../../../../application/_old/3-deliver/haipipe-application-deploy/SKILL.md`
  The ship step, still a stub; implementation lands here and must keep the gate.

📥 **Input files** · what the work reads

- `../../../PaperSkillBoard-260725/board.md`
  QB9@paper, the precedent this page mirrors: candidates a human reviews before anything becomes the submission.

## Glossary

- 📄 **Artifact**: one drafted message variant in `0-artifacts/`, carrying its status (draft, reviewed, deployed) in frontmatter.
- 🅰️ **Adopted A**: a design-advice entry from 1d-advice that the artifact chose to execute; the first hop of the trace chain.
- ⚓ **Anchor**: the evidence a ledger claim points back to; the last hop of artifact to A to C to anchor.
- 🕳 **GAP**: a claim-ledger status meaning the claim has no settled evidence yet; an artifact may not cite a GAP claim as fact.
- 🪜 **1a**: the descriptions rung of the evidence ladder (1a-descriptions, 1b-themes, 1c-claims, 1d-advice); deployment results land here as new data.

## Log

260802 · Page created: the three 3-deliver skills quoted as they stand, QB9@paper's promote asymmetry mirrored as the ship gate, and two rulings put in front of JL: the 3-deliver re-bucketing and who may say go for production.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0