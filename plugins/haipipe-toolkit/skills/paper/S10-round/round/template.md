<!-- TEMPLATE · ONE DATED ROUND = ONE S PAGE.
     create-page.py lays the Board shell from this file; DRAFT fills it and DELETES every
     RULE comment as it satisfies it. A RULE comment never ships in the filled page.
     Gate: grep -c 'RULE:' on the filled page must print 0.

     WHAT A ROUND IS: one coherent batch of iterative work: a coauthor pass, an editor
     letter, an external review cycle, an internal sweep. The page is the round's ONLY
     record: there is no latest.md, todo.md, decisions.md, discussion.md, or applied.md.
     Received material (a reviewer letter, a memo) is copied or linked BESIDE this page
     in 0-lifecycle/S10-round/, only when the user supplied it.

     NO markdown pipe tables anywhere: every would-be table is record lines. -->

# S Round <n> · <vYYMMDD> <short purpose>
state: 🔴 OPEN
owner: JL
method: land the feedback verbatim, triage it to a ledger, route the work, record what applied, close with a receipt
requires: <the S pages this round reopens or reads, comma separated; grows during triage>
style-from: S-Open-Pitch
provides: <what the close receipt certifies, one line>

<!-- RULE: `state:` begins with one of the Board's FOUR values: 🔴 OPEN · 🟡 PARTIAL ·
     ✅ SETTLED (close approved) · ⏸️ ON HOLD. A short readable detail may follow the emoji;
     the evidence belongs in `## States`. ✅ only after the human approves the close. -->

## Question
Has every item of <this batch's feedback> been applied, answered, or explicitly parked, and does the close receipt prove it?

<!-- RULE: the paragraph under the question names the trigger and the stake: who sent what,
     and what the paper owes back (a revision, a response, a decision log). -->
<one paragraph: the trigger, the scope, and what closing this round delivers>

## Boundary
- ✅ Covered here
  This one batch: intake, coverage ledger, decisions, applied changes, the response when one is owed, and the close receipt.
- ↪ Covered elsewhere
  Reopened S pages keep their own authority and gates; claim status lives only in the claims page; build outputs belong to the door's build verbs; the NEXT batch is the next round page.

## Content

### Source and intake

<!-- RULE: what arrived, from whom, dated; quote or link, never paraphrase at intake.
     Interpretation happens on the ledger, and every ledger quote anchors back here. -->

Source: <who/what, date>

Purpose: <one line: what this batch must settle>

Received material: <link to the letter/memo beside this page, or "none (internal round)">

### Coverage ledger

<!-- RULE: ONE record block per atomic item; record lines, never pipe tables. Atomize: one
     concern = one item, even when the letter bundles several into a paragraph. Ids: R2-C1
     grammar for reviewer items, <initials>-<n> for internal feedback. Every item ends in
     exactly one closing state: applied | answered | parked. Nothing silently disappears. -->

- <id> · <short title>
  quote: "<the anchoring words, verbatim>"
  kind: <claim | display | placement | wording | evidence | response | build | other>
  severity: <critical | major | minor>
  decision: <accept | narrow | decline> (<who ruled, date>)
  target: <owning S page / stage route / this page's Response / parked: reason>
  state: <open | applied | answered | parked>

### Decisions

<!-- RULE: accepted rulings only, one line each, with who ruled and when. A decision made in
     chat is written here so it enters the comment lifecycle; ledger rows point at these. -->

- <date> · <who> · <the ruling, one sentence>

### Applied changes

<!-- RULE: REVISE appends as items land: what changed, where, which ledger item it closes.
     Unresolved work stays visible on the ledger; this division records only what happened. -->

- <date> · <ledger id> · <what changed, in which S page/file>

### Response

<!-- RULE: only when this round answers external readers. Draft per ../rebuttal-craft.md:
     opener with global resolutions, per-reviewer numbered replies (answer -> evidence ->
     implication), short closing. Every factual sentence has a provenance source; every
     promise maps to a ledger item. Keep the paste-ready character count beside the venue
     limit. Write "not an external round" when no response is owed. -->

<the reply text, or "not an external round">

### Close receipt

<!-- RULE: CHECK writes this at close, after human approval: ledger counts by state; pages
     reopened and their gate states; the build/candidate produced, if any; forward pointers
     the NEXT round inherits. -->

Ledger: <n applied · n answered · n parked of N total>

Reopened pages: <S-… list with their current gate states, or "none">

Build: <the candidate/PDF this round produced, or "none">

Forward: <parked items the next round inherits, or "none">

## Aims

<!-- RULE: Aims names this round's intended outcomes. Known triage/apply work and the human
     close gate are ordinary Aim records; use a P record only for an unresolved evidence
     question. Numbers come from the bank, never from the agent; route uncertainty through
     PROBE (MATCH first; the ceiling is probe_depth, raised only by a human). -->

### Round output
- A1.1 · Triage every intake item onto the coverage ledger with a decision and a target.
  **Done when:** Every item appears exactly once and names its route or its parked reason.
- A1.2 · Apply the accepted items and record each change.
  **Done when:** Applied changes lists every landed edit with the ledger id it closes.
- A1.3 · Pass this round's close gate.
  **Done when:** JL approves the close summary; state flips to ✅ and the receipt is written.

### P · Stage questions
- P<n> · Q-Round<unit>-<n> · <question title>
  **Done when:** The answer has landed, been interpreted, and the ledger row it serves is closed.
  **Description:** <what the question wants to know, one sentence per line>
  **Reason:** <which ledger item(s) / response sentence(s) cite this id, and why each matters if the assertion is wrong>
  **Probe:** not opened yet
  **Answer:** <empty in DRAFT; PROBE fills it from the answering QA file>

## States

<!-- RULE: the current fact of the round, one short block: what is open, what blocks close,
     what the human last ruled. Re-derived from the ledger, never a second queue. -->

<current fact, a few lines>

## Files

- `0-lifecycle/S10-round/S-Round-<n>-<vYYMMDD>.md`
  This page: the round's only record.
- `<received letter/memo file>`
  Beside this page, only when supplied.

## Log

<!-- RULE: dated triage/apply events, resolved comment threads moved here verbatim, and the
     close gate receipt (actor + date). Newest first. Never rewrite an existing row. -->
