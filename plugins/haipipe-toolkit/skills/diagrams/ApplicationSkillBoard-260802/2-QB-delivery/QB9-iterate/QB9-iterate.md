# Delivery Iterate: A/B results come back as fresh data

state: 🔴 OPEN
owner: JL
method: keep one A/B batch together from deploy to ladder refresh, mirroring the paper board's round rule

## Opening

What does the Iterate concern deliver, and how does staleness propagate when A/B results come back?
A deployed artifact generates live numbers, and Iterate lands them as fresh D entries in 1a, the ladder's bottom rung.
The hard part is that new numbers silently invalidate the themes, claims, and advice built on the old ones.
This page states what one iteration keeps together, and how a [STALE] stamp re-opens exactly the affected rungs.

**What the words mean**: an A/B batch is one deployment's results read together, such as the per-variant click rates from one SMS send; the 1a refresh lands each metric as a dated, anchored D entry in `0-lifecycle/1a-descriptions/1a-descriptions.md`; the ladder is the evidence chain 1a-descriptions to 1b-themes to 1c-claims to 1d-advice.

**Where this page sits**: the Deploy concern in this group owns getting the artifact live; this page starts where deploy ends, at the first live numbers, and it ends when the ladder has absorbed them.

**The intentional delta vs paper**: the paper's batch (QB10@paper) is opened by reviewers judging text, and the feedback lands as prose revisions; the application's batch is opened by the deployed artifact itself, and the feedback lands as data, which is why it backfills 1a instead of editing any downstream rung directly.

**Why it matters**: without the ladder-first rule, a winning variant gets promoted on numbers no claim ever absorbed, and the next iteration argues from evidence the deployment already contradicted.

## Writing Style

How this page must be written; edit to it.

**Language and sentences**: English only. One sentence per source line. No em-dashes; use a colon, a comma, or a new sentence.

**This page DESIGNS; an intervention folder SHOWS**: state what the concern requires of any intervention, never what one intervention happens to have today. Where a real intervention falls short, write it as a dated gap with an owner.

**Say Iterate for the loop and round for the record**: the loop is the concern; the dated `vYYMMDD/` folder is where one pass of it is recorded. A sentence that calls the loop a round has collapsed the design into its bookkeeping.

## Diagram

**The outer loop**: one A/B batch, from deploy to the next ladder refresh.

```text
        🚀 deploy (maturity: deployed)
             │
             ▼
   ┏━━━━ ITERATION n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ 📥 ingest     A/B results · metrics ·          ┃
   ┃               feedback → 1-rounds/vYYMMDD/     ┃
   ┃ 🪜 backfill   each metric → dated D entry (1a) ┃
   ┃ 🏷 stamp      [STALE] on downstream T · C · A  ┃
   ┃ 🚦 triage     decisions → artifact · pitch ·   ┃
   ┃               claims · display · advice        ┃
   ┗━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                     ▼
        ITERATION n+1 (iterating) … 🛑 kill criterion → retired

  🪜 gate      ladder first ── no decision before its metric is in 1a
  🔁 loops     outer weeks · middle one round (days) · inner one probe (hours)
```

## Content

### 1 · The delivery contract

**What Iterate owes**: a batch a later reader can follow from deploy to the ladder refresh it forced.

```text
  📥 CONSUMES               📤 PROJECTS TO             🚪 GATE
  A/B results · metrics ━▶  vYYMMDD round record  ━▶   ladder first:
  clinician feedback        fresh D entries in 1a      every metric is a
  0-seed kill criteria      [STALE] stamps on T·C·A    dated D entry before
  2-pitch testable goal     triage routes · maturity   a decision cites it
```
📌 Establishes the A/B batch as the unit, and what must be true before any decision leaves it.

| Field | Contract |
|---|---|
| Lifecycle | Everything after deploy: each batch of live results and the refresh it forces. |
| Authority | One dated round folder per batch (`1-rounds/vYYMMDD/`), with decisions and an applied log. |
| Projects to | Fresh D entries in 1a, [STALE] stamps on downstream rungs, triage routes, maturity. |
| Skills | `haipipe-application-iterate`, `haipipe-application-round`, the 1a refresh path. |
| Consumes | A/B results, engagement metrics, feedback, plus 0-seed kill criteria and the 2-pitch testable goal. |
| Gate | Ladder first: every metric is a dated D entry in 1a before any decision cites it. |
| Open gaps | Kill authority and stamp reach are unruled; both sit in Decision Now. |

#### 1.1 · Backfill the ladder first, then extract decisions
(fresh numbers are new data before they are verdicts, and the order is the whole rule)
Step 4 of the iterate skill lands each metric as a dated, anchored D entry in `0-lifecycle/1a-descriptions/1a-descriptions.md` before any decision is extracted.
The order matters because every decision cites evidence: promote v2, drop v1, move a claim from GAP to supported.
Skip the backfill and the claim ledger keeps citing pre-deployment evidence while the artifact changes on numbers the ladder never absorbed.

#### 1.2 · One batch stays together, and the round folder is the carrier
(the application transplants the paper's batch rule and swaps the contents)
QB10@paper keeps one batch of reviewer feedback together from review to resubmission.
Here the batch is one A/B batch, and the dated `1-rounds/vYYMMDD/` folder holds it whole: `discussion.md` the raw numbers, `decisions.md` the verdicts, `todo.md` the routes, `applied.md` the backfill log.
The iterate skill writes only round files; every change to a lifecycle artifact is routed through the stage skill that owns it.

### 2 · Staleness propagates up the ladder

**How a refresh climbs**: a new D entry, and the rungs it re-opens.

```text
  🪜 THE LADDER, read bottom-up

  1a D   ── refreshed ──▶ 🏷 new dated entry
   │ cited by
  1b T   ──▶ [STALE] when its D id moved
   │ tags
  1c C   ──▶ [STALE] when its theme went stale    ← chain reading
   │ derives
  1d A   ──▶ [STALE] when its claim went stale    ← chain reading

  🎯 reach   one hop vs whole chain ── open ruling (Decision Now)
```
📌 Establishes what a [STALE] stamp does, and names the one ambiguity that stops it being implemented.

#### 2.1 · The stamp re-opens; it does not judge
(a stamped entry may survive its re-read unchanged)
[STALE] marks an entry whose evidence moved; it says re-read, not wrong.
A stamped theme can be re-confirmed against the fresh D entries and keep its wording.
That is what re-opening exactly the affected rungs buys: an untouched D id keeps its themes, claims, and advice green, so a refresh never resets the whole ladder.

#### 2.2 · The skill's wording and the chain intent disagree
(the literal reading of "cite the refreshed ids" never reaches 1c or 1d)
The iterate skill stamps downstream T, C, and A entries "that cite the refreshed ids".
But the ladder's citation rule runs one rung at a time: a theme cites D ids, a claim is theme-tagged, an advice entry derives from a claim.
Read literally, only themes ever cite a D id, so claims and advice would never be stamped; read as a chain, the stamp walks D to T to C to A.
Which reading holds is JL's ruling, parked in Decision Now.

### 3 · The outer loop and the maturity words

**Three nested loops**: where Iterate sits, and the state words it moves.

```text
  🔁 THREE NESTED LOOPS

  🌍 outer    weeks   deploy → results → 1a refresh → redeploy   ← THIS PAGE
  📅 middle   days    one round: open → discuss → triage → close
  ⏱ inner    hours   one probe question: dispatch → answer

  🌡 maturity  deployed → iterating → retired
```
📌 Places Iterate as the weeks-scale loop and pins the maturity vocabulary it drives.

#### 3.1 · Iterate owns the outer loop only
(the middle and inner loops are carriers this page names but does not run)
The outer loop runs on weeks: deploy, collect live results, refresh 1a, re-settle the stamped rungs, then redeploy or retire.
The middle loop is one round on days, open through close; Iterate opens one as its carrier (step 1 of its workflow) and the round skill runs it.
The inner loop is one evidence question on hours, dispatched through the probe machinery by the stage skills; Iterate never runs it, it only feeds the ladder whose gaps raise those questions.

#### 3.2 · Maturity: deployed, iterating, retired
(the loop's own state word, kept in STATUS.md, and one write is missing)
An intervention that shipped is deployed; the first ingested batch should move it to iterating; a met kill criterion ends it at retired, with the reason recorded.
Today the iterate skill writes only the last word: step 7 sets maturity to retired, and no step sets iterating on first ingest.
Who may write retired is the first Decision Now row; that nothing writes iterating is a gap the skill owner closes either way.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · The ladder-first gate binds every iteration.
  **Done when:** no decision in a round's `decisions.md` cites a metric that is not already a dated D entry in 1a.
- A1.2 · One A/B batch is followable end to end.
  **Done when:** a later reader can reconstruct one batch from a single `vYYMMDD/` folder: raw numbers, verdicts, routes, and the backfill log, with nothing split across rounds.

### A2 · 🪜 Staleness propagates up the ladder
- A2.1 · A refresh re-opens exactly the affected rungs and nothing else.
  **Done when:** the stamp's reach is ruled in Decision Now, the 1a refresh implements that ruling, and a test refresh stamps every entry the ruling names and no other.

### A3 · 🔁 The outer loop and the maturity words
- A3.1 · Maturity moves from deployed to iterating to retired, written by the lifecycle rather than by hand.
  **Done when:** the first ingested batch sets iterating, and retired is written only per the kill-authority ruling, always with a reason.

## States

### Decision Now

- [ ] 🗣 Does a met kill criterion retire the intervention by itself, or only flag it for JL?
      📍 `Part 3` the maturity words and who writes them
      🔔 `Why now` the iterate skill disagrees with itself: its trigger table flags a met criterion for shutdown, and its step 7 writes maturity retired directly.
      `A ·` auto-retire: the machine writes retired the moment the criterion is met, which commits you to trusting the pre-registered criterion with no second look.
      ⭐ `B ·` flag only: iterate raises the flag and JL writes retired, which commits you to a human ruling on every shutdown and accepts the delay; CC recommends B because retiring is the loop's one irreversible move, and the board rule is that a machine proposes where a human rules.
      🛑 `Blocks` nothing on this page; A3.1 records the answer when it lands.
      🤖 `If nobody answers` B: iterate flags and never writes retired on its own.

- [ ] 🗣 Does a [STALE] stamp travel one hop or the whole chain?
      📍 `Part 2` the staleness propagation rule
      🔔 `Why now` the skill stamps downstream entries "that cite the refreshed ids", and a claim cites a theme rather than a D id, so the literal reading never reaches 1c or 1d.
      `A ·` one hop: only entries citing a refreshed id directly are stamped, which commits you to advice staying green while its foundation moves.
      ⭐ `B ·` whole chain: the stamp follows the citation chain from D through T and C to A, which commits you to chain-walking in the 1a refresh and more stamps per batch; CC recommends B because the ladder's own citation rule makes one-hop stamping structurally unable to reach 1d.
      🛑 `Blocks` A2.1: the stamping rule cannot be implemented or tested until its reach is ruled.

### A1 · 📜 The delivery contract
- 🧠 A1.1 · The rule is written (skill step 4, the Gate row here); verifying it waits on a live batch, and nothing read for this page shows one yet.
- 🧠 A1.2 · The carrier exists: the round skill scaffolds the five-file `vYYMMDD/` folder and the `latest.md` pointer; whether a real batch stayed whole waits on the same live batch.

### A2 · 🪜 Staleness propagates up the ladder
- 🧠 A2.1 · Waiting on the stamp-reach ruling; the skill's one-hop wording and the chain intent disagree (§2.2).

### A3 · 🔁 The outer loop and the maturity words
- 🧠 A3.1 · Waiting on the kill-authority ruling; today step 7 writes retired directly, and no step writes iterating.

## Files

### ⚙️ Engines
- `../../application/4-iterate/haipipe-application-iterate/SKILL.md`
  The loop itself: ingest, ladder backfill (step 4), triage (steps 5 and 6), kill handling (step 7); the ladder-first rule changes here.
- `../../application/0-enter/haipipe-application-round/SKILL.md`
  The carrier: scaffolds `1-rounds/vYYMMDD/`, routes todo items to the owning stages, closes the round.

### 📥 Input files
- `../PaperSkillBoard-260725/2-QB-delivery/QB10-round/QB10-round.md`
  The paper precedent (QB10@paper): one batch kept together from review to resubmission, the rule this page transplants.

## Glossary

- 🔁 **Iterate**: the outer loop of the intervention lifecycle: one deployment's results ingested, anchored in 1a, and triaged back into the stages.
- 📦 **A/B batch**: one deployment's live results read together, such as the per-variant click rates from one SMS send.
- 🪜 **Ladder**: the venue-free evidence chain 1a-descriptions to 1b-themes to 1c-claims to 1d-advice.
- 🏷 **[STALE]**: the tag the 1a refresh stamps on a downstream entry whose evidence moved; it forces a re-read and passes no verdict.
- 🌡 **Maturity**: the intervention's one-word lifecycle state in STATUS.md; this concern moves it through deployed, iterating, retired.
- 📅 **Round**: one dated `1-rounds/vYYMMDD/` folder recording one batch from intake to close.

## Log

260802 · Page created: Iterate stated as the outer loop with the ladder-first gate and the staleness chain, and two rulings put to JL (kill authority, stamp reach).
