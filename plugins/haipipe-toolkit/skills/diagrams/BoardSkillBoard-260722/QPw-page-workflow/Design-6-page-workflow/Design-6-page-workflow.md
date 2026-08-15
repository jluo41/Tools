# Design-6 · Page Workflow (Agent creator v0.6.0, Agent reviewer v0.7.0, Agent orchestrator v0.1.0)
state: 🟡 in flux · three hands at three maturities; the orchestrator has never run AS an agent
owner: CC
page-type: design
method: one design page for the workflow's dispatched hands; unit snapshots in skill/ via skillpage.py plug; every section authored (merged from three unit pages 260815)

## Opening
Who runs a page's DRAFT, PROBE, REVISE and CHECK when no person is in the loop, and what may each hand touch?

One design answers it with three dispatched agents, and the split is the design: the producer writes and never judges, the judge reads and never repairs, and the controller routes and never edits prose.
A single agent doing all three would approve its own work, which is the failure CHECK exists to prevent.
This page owns the design; each unit's contract file is the authority on its own procedure and ships from `board/agents/`.

**Covered elsewhere**: `QPw1` owns the page's time axis the hands move through; the four phase contracts ship as skills and their page is still owed (this group's intro carries that debt); `QF1` owns the gate the reviewer serves.

## Diagram
**One loop, three hands**: who acts at each phase, and what each may never do.
```text
            🔁 RUN · Design-8's controller, bounded, receipted
            ┌───────────────────────────────────────────────┐
            │  ✍️ DRAFT / REVISE          🧑‍⚖️ CHECK           │
            │  the creator, one page      the reviewer,      │
            │  per fresh context          read-only, fresh   │
            │  never rebuilds ·           never repairs ·    │
            │  never CHECKs               returns a verdict  │
            └───────────────────────────────────────────────┘
   📦 skill/ holds each unit's contract surface, plugged and versioned
```

## Content
### 1 · The design in one screen
**Three units, one rule each**: the sentence a unit may never cross is its identity.
```text
  ✍️ creator       writes ONE page in a fresh context · batch = N creators,
                   one page each · self-checks are evidence, never approval
  🧑‍⚖️ reviewer      the fresh-context judge: mechanics, cold-read, Openings
                   in board order · CLOSE REVISE PROBE DRAFT HOLD · no writes
  🔁 orchestrator  the non-interactive RUN target: drives the bounded
                   Workflow, stores _runs/ receipts, calls the auditor
```
The live units ship from `board/agents/`, one .md each; this page's `skill/` plugin holds the three plugged snapshots its judgments are about.

### 2 · Selection record · one design, several units
**The candidates**: how many pages a three-handed design deserves.
```text
  🅰 one page per unit (lost)         🅱 one page per DESIGN (won)
  three pages saying one design's     the design argued once · each
  thoughts three times                unit a division · versions in
                                      the title, refreshed by plug
```
This page is the specimen of the 260815 ruling that a Design relates to several skills or agents.
🅰 lost the same way the mirror kind lost: pages that share one subject converge on one prose and decide nothing separately.
The base selection that retired the mirror kind is recorded once, on `Design-3-haipipe-page` Content §2, and this page adopts it.
Disposition of 🅰: the three pre-merge pages are archived whole, and their ids resolve through `## Links`.

### 3 · The creator, and what the caller still owes
The unit is written and proven: the 260802 fan-out drove six packets through six fresh creators.
What is missing is the caller's half, and both open aims below are that debt: packet assembly is still done by hand, and a dispatch that dies mid-batch leaves the caller re-reading files to learn which packets completed.

### 4 · The reviewer, and the pass it has never run
The unit is the family's independence mechanism: fresh context, no write tools, verdict only.
Its consecutive-Openings pass, the reason 0.4.0 exists, has never run on a real batch, and one has been waiting since 260802.
A 260729 remark, "don't need to have the review agent", was said while one dispatch ran and has never been ruled as run-scoped or unit-scoped; three written things go stale together if it meant the unit.

### 5 · The orchestrator, reasoned but unexercised
The one live RUN on 260805 could not reach the Workflow tool, so a session emulated this controller by hand.
Nothing has yet run the charter AS an agent, so its stop rules and return contract are design, not record.
The stored receipt also carries no `audit:` field, so whether the auditor passed that run is not on the record.

## Aims
- [ ] 🚚 The caller's fan-out half lands in `haipipe-board`
      Packet assembly from an approved proposal table, and the serialized tail run once, instead of by hand as on 260802.
- [ ] 🩹 A dispatch that dies mid-batch is recoverable
      The caller learns which packets completed without re-reading the files.
- [ ] 🧑‍⚖️ The reviewer's consecutive-Openings pass runs on a real batch
      The eight roster Openings of 260802 are the waiting batch.
- [ ] 🤖 The 260729 "don't need the review agent" remark is ruled
      Run-scoped or unit-scoped; three written things depend on the answer.
- [ ] 🧭 The orchestrator's charter is dispatched rather than emulated
      One RUN through the agent itself, exercising its stop rules and return contract.
- [ ] 🧾 The auditor's verdict reaches the receipt it audits
      The return contract's `audit:` field appears in a stored receipt.

## States
Merged 260815 from the three unit pages; their full pre-merge records are archived whole.
The creator is the most proven hand (a real six-page fan-out), the reviewer is proven but has one pass never exercised, and the orchestrator has never run as itself.
Nothing here is contested; everything here is waiting on a run.

## Log
- 260815 1500 · [REVISE-CC] merged from Design-6/7/8 (JL 260815: "one Design can relate to several skills or agents"): one design page, three plugged units, versions in the title; the three originals moved to `_archive/` whole.
