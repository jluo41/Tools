# The evidence channel: the application cut of the wall

state: 🟡 PARTIAL
owner: JL
method: read the two application probe documents and the checker against the paper twin, keep only the deltas, and put the one open ruling to JL

## Opening
**Current ruling (260817)**: this page is now a legacy analysis of the old Application-local evidence channel. The canonical Application family owns no Probe and no evidence pool. Probe lives on Task/Insight Pages, where it reads Task and Discovery folders. Application reads only settled Insight Pages through PageX; an unresolved factual need routes back to `/haipipe-task insight` instead of creating an Application probe.

How does an intervention's question cross the wall into the task/discovery bank, and what is the application's own in that crossing?
The wall is a clean context: the question leaves as a stake-stripped string, and the answer returns as a file bound by path.
That model belongs to /haipipe-probe, and the paper already ruled its own cut of it as QA5@paper.
This page rules the application cut: the topic pool, the 1c-only claim status, the venue bar, and the one bank door.

**The words in the question**: an intervention is one application folder running the lifecycle under `0-lifecycle/`, such as an sms refill-reminder campaign.
The task/discovery bank is the project's `tasks/` and `discoveries/` trees, answering in QA files such as `tasks/X03_refill_timing/01_window_scan/QA/1-response-window.md`, and it never learns an intervention exists.
The wall is the clean context between the intervention's claim and that evidence: what crosses is a q-executor, the question with its stake stripped.

**Where this page sits**: QA5@paper is this page's twin on the paper board, and it rules the paper cut of the same crossing.
The model itself, the probe-file anatomy, the QA state line, the cost ladder, and the two LAWS, is /haipipe-probe's; this page cites it and rules none of it.
What is left for this page is only what the application does differently.

**Why it matters**: every number and citation in an artifact a patient or a colleague sees arrives through this one door.
The application's extra exposure is laundering: the claim ledger sits one prose hop above the probe file, and §4 shows nothing hard connects them, so a supported claim can rest on an answer nobody read back.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Cite the twin as a plain token**: the paper board's page is written QA5@paper, and its content is pointed at, never re-explained here.

**Never restate the shared model**: the probe-file anatomy, the QA state-line contract, the cost ladder, and the two LAWS belong to /haipipe-probe.
Cite them; a copy here becomes a second authority the day the layer moves.

**Name the four vocabulary words exactly**: Q-consumer, q-executor, a-executor, a-consumer.
They differ by one letter and one hyphen, and a page that blurs them makes the wall unreadable.

**A drift names both sides**: this page records three places where the application sources disagree, and each one quotes both files and the newer date rather than silently picking a winner.

## Diagram

**The application crossing**: what leaves the intervention, what returns, and what never leaves.

```text
 💊 THE INTERVENTION                         🏦 THE BANK, across the wall
 ┌─────────────────────────────┐            ┌────────────────────────┐
 │ 0-lifecycle/1c-claims/      │            │ <project>/tasks/       │
 │   🔒 the claim STATUS       │            │ <project>/discoveries/ │
 │   supported | weak | GAP    │            │ probe-unaware ·        │
 │   never leaves this file    │            │ owned by /haipipe-task │
 │ stage docs · ## Q-consumer  │            │ and /haipipe-discovery │
 └────────────┬────────────────┘            │                        │
              ▼                             │ <folder>/QA/           │
 ┌─────────────────────────────┐            │   <n>-<slug>.md        │
 │ 1-probes/PP03_<topic>/      │            │   state: working |     │
 │   QX1_<slug>.md · ## QX1    │            │   answered | superseded│
 │   ### q-executor ━ STRING ━━━ 🕊 agent ━▶│                        │
 │   ### q-consumer            │            │                        │
 │   ### bank binding · target: ━ BY PATH ━▶│ points at that file    │
 │   ### a-executor ◀━━━━━━━━━━ the answer  │                        │
 └─────────────────────────────┘  as a FILE └────────────────────────┘
```

## Content

### 1 · The pool: one folder per topic, footnote-numbered

**The pool on disk**: the shape the checker enforces since the folder-only cutover.

```text
 📁 1-probes/                    one flat pool · no per-stage folder
   ├── PP01_<topic>/             📂 one folder per TOPIC
   │   ├── QX1_<slug>.md         📄 one file per q-executor
   │   └── QX2_<slug>.md         🏷 each opens with its ## QX<n> entry
   └── PP02_<topic>/
 🔢 numbering     intervention-local footnotes · ls 1-probes/ decides
 🚫 in the bank   no PP id in any QA filename · a checker FAIL
```
📌 This part fixes the pool's shape on the page and records that one of the two application documents still draws the retired shape.

#### 1.1 · PP numbers are footnotes, not ledger ids
(the numbering authority is ls, and nothing reconciles across interventions)
`fn/probes.md` calls PP numbers intervention-local footnote numbers: there is no ledger, and no PP id ever crosses to the bank, so two interventions may both carry a PP03 with nothing to reconcile.
The checker makes the second half hard: a PP id in a bank QA filename FAILs as `pp-id-in-bank-filename`.

#### 1.2 · The topic is a folder, and one document still says file
(two application sources, two shapes, and the checker sides with the folder)
`check-probe-cards.sh` globs `1-probes/PP*/*.md`, and its header states that the flat single-file `1-probes/PP*.md` was retired at the folder-only cutover.
The worker's own description agrees: one q-executor per `QXn_<slug>.md` file inside `PPNN_<topic>/`, each file carrying its `## QX<n>` entry with the four `###` subsections.
`fn/probes.md` still draws `PP01_refill-timing.md` as a flat file and says one file per topic, which is the retired shape.
`A1.1` holds the repair.

#### 1.3 · Harvest folds inline, and a sidecar is a FAIL
(the application delta around the pool: no lanes, no sidecar docs)
The answer's numbers and citations land inline in the entry's `### a-executor`, each anchored to `target:`.
There are no `values:`, `sources:`, or `displays:` lanes and no sidecar docs: the checker FAILs any lane line as `harvest-owed`, and its sidecar pass was removed on 2026-07-18 because nothing was left to check.

### 2 · The loop and the one door

**Five steps, one door**: what each step does, and where the wall sits.

```text
 ① ORGANIZE    question → entry · q-executor frozen, stake stripped
 ② MATCH       read-only grep of the bank · most entries stop here
 ③ DISPATCH    target: NEW only · handed to the collector agent
 ④ POINT       target: = the answering QA FILE · opened, never trusted
 ⑤ INTERPRET   ### a-executor → stage-doc a-consumer → 1c flips
 🚪 the door    haipipe-probe-q-executor-agent · clean context = wall
```
📌 This part carries the loop in the application's own words and records who owns each step, including the one step whose owner is stated two ways.

#### 2.1 · Match before dispatch
(the bank fills from the executor side, so a NEW dispatch is the exception)
The bank fills autonomously from the executor side, so in a healthy project most answers already exist before anyone asks.
A probe folder whose every entry is NEW-to-dispatch is a smell: either the MATCH was lazy or the bank is starving, and the run's reply must say which.

#### 2.2 · The collector agent is the only bank door
(the stake-free middle, and why a stage never dispatches inline)
The agent sends each `### q-executor` verbatim to the task or discovery orchestrator, writes the returned `target:`, and reports QA-path, in-flight, or failed per entry.
It never reads the intervention's registries, the stake, or the stage-doc Q-consumers; its clean context is the wall.
A stage never calls a bank orchestrator itself, because inline results land nowhere reviewable and die with the reply.
The PROBE worker writes nothing under `tasks/` or `discoveries/`, ever: no stub, no mailbox.

#### 2.3 · Two application-only closes: T1 LOCAL and the display reroute
(what an intervention may answer from its own registries, and what it may not collect)
T1 LOCAL is a closed whitelist of the intervention's own registries: entries already read, `0-artifacts/` display units, and the 1c campaign rows.
An entry fully answered there closes `answered-local` with no dispatch, and it adopts the pointer, never the verdict, since a reused value re-verifies against its original source at harvest.
A question asking for a display unit that does not exist is rerouted, not collected: it becomes a request row for the display stage.

#### 2.4 · Who authors ① and ② is stated three ways
(one file disagrees with itself, and the sibling document sides with its body)
The worker's description, dated 2026-07-20, says ①ORGANIZE and ②MATCH moved into PROBE with the removal of the DRAFT gate, and that DRAFT now raises questions and nothing else.
The same file's body says ① and ② are done at DRAFT and are the worker's precondition.
`fn/probes.md` agrees with the body: DRAFT authors the plan, PROBE runs it forward.
`A2.1` holds the repair; the loop above stands either way, since every step still runs and only the phase label moves.

### 3 · What stays behind: the status and the bar

**What never crosses**: the judgment and the depth both stay in the intervention.

```text
 🧾 1c-claims.md   the ONLY home of a claim's STATUS
    vocabulary     supported | weak | GAP · written by the AUTHOR
    same pass      the C-line and its Evidence Campaign row flip together
 🎚 the bar        light | medium | full · read by the venue gate
 🚫 probe entry    carries the evidence · never the judgment
```
📌 This part places the two things the crossing must never move: the claim's status and the decision of how settled is settled enough.

#### 3.1 · The author judges, in the ledger, in one pass
(a probe is communication, not judgment)
A claim's status lives in `0-lifecycle/1c-claims/1c-claims.md` and nowhere else: the author flips the C-line and its Evidence Campaign row in the same pass, and never writes a status into a probe file.
There is no review gate on a probe and no verdict block; the one standing check is the overclaim rule, never causal from associational evidence.

#### 3.2 · Two status triples are in print
(the ledger's vocabulary and the probe documents' vocabulary disagree)
The ledger's vocabulary is supported, weak, GAP.
Both probe documents still write supported, refuted, inconclusive with a confidence.
Nothing breaks today, because the probe documents only name where the status goes, but the first author who copies their triple into 1c writes a status the claims stage does not define.
`A3.1` holds the repair.

#### 3.3 · The venue sets how much must settle
(the same campaign can pass one bar and fail another with no evidence changed)
The venue gate reads the evidence campaign against its settlement bar: light, medium, or full.
The depth is not the ladder's to choose, so the same claim ledger can satisfy a light bar and fail a full one with nothing about the evidence changed.
The bar is venue-aligned, which means retargeting the intervention re-asks how settled its claims must be.

### 4 · The teeth: one hard set, and the links without one

**Where the checker bites**: every tooth sits inside 1-probes/ or the bank.

```text
 🦷 hard teeth · check-probe-cards.sh      🍮 prose only
 ─────────────────────────────────────    ──────────────────────────────
 planned → FAIL · answered-not-read        stage-doc a-consumer written
 read → the target is OPENED and read      1c C-line + campaign flipped
 commissioned → eta test + loop-closer     everything above the probe file
 LAW 2 on both surfaces · one pattern set
 lying receipts · zombies · no tables
```
📌 This part records the hardening gap the page puts to JL: probe state is checked hard, and the consumption of an answer is checked only by prose.

#### 4.1 · What the checker verifies
(the entry, the target, and the bank, all opened)
`planned` FAILs as probe-not-run, `answered` with an empty `### a-executor` FAILs as answered-not-read, and a `commissioned` entry whose target already answered FAILs as commissioned-target-answered instead of sitting green until its eta expires.
Since R19/R20 the target's own state line is read: existence is no longer enough, so a `read` entry over a `working`, superseded, or stateless QA file FAILs.
LAW 2 runs on both surfaces with one shared pattern set, because two hand-copied regex sets once drifted into missing the same canonical leak.
On the bank side, an `answered` file with an empty `## Answer` is a lying receipt and a `working` file past its TTL is a zombie, and both FAIL.

#### 4.2 · What no script reaches
(the consumption links the worker requires only in prose)
Every tooth above bites inside `1-probes/` or the bank; the script never opens a stage doc or the 1c ledger.
The worker's ⑤ requires the stage-doc a-consumer and the ledger flip, and its proof is lines in the worker's own reply, which is transcript discipline rather than a gate.
So a green PROBE can sit over an answer that landed, was copied into `### a-executor`, and was never consumed: no a-consumer written, no C-line flipped, nothing red anywhere.

#### 4.3 · The ruling this leaves open
(harden the links, or accept the prose)
Whether those links get their own teeth is JL's call, and the `### Decision Now` row in `## States` carries the options.

## Aims

### A1 · 📁 The pool: one folder per topic, footnote-numbered
- A1.1 · The two application probe documents draw the same pool shape the checker enforces.
  **Done when:** `fn/probes.md`'s location figure shows `PP<NN>_<topic>/QXn_<slug>.md`, and no application source still calls the pool one file per topic.
- A1.2 · Harvest stays inline, and no lane or sidecar survives a green gate.
  **Done when:** the checker FAILs any lane line and carries no sidecar pass.

### A2 · 🚪 The loop and the one door
- A2.1 · One phase owns ①ORGANIZE and ②MATCH, in every application source.
  **Done when:** the worker's description, its body, and `fn/probes.md` name the same author for ① and ②.
- A2.2 · The one-door rule is on the board in the sources' own words.
  **Done when:** §2.2 names the agent, what it may never read, and the rule that a stage never dispatches inline, each traceable to the worker SKILL.

### A3 · 🧾 What stays behind: the status and the bar
- A3.1 · One status vocabulary is in print across the application documents.
  **Done when:** the probe worker and `fn/probes.md` write the ledger's triple, or the ledger adopts theirs, and no application document carries both.

### A4 · 🦷 The teeth: one hard set, and the links without one
- A4.1 · JL rules whether the consumption links get hard teeth or stay prose-enforced.
  **Done when:** the Decision Now row is answered and the ruling lands in this page's `## Law` with the date.

### P · 🏁 Page-level
- P1 · Every delta on this page names the shared rule it varies, so the page can never become a second authority for the model.
  **Done when:** each Content division cites /haipipe-probe or QA5@paper for the model piece it varies, and none restates the anatomy, the QA state line, or the two LAWS.

## States

### Decision Now
- [x] 🗣 Do the ladder's consumption links get hard checker teeth, or stay prose-enforced? **Superseded:** the canonical Application path has no ladder-local consumption links to check.
      📍 `Part` 4 · the teeth
      🔔 `Why now` this page records that every existing tooth bites inside 1-probes/ or the bank, so a green PROBE can sit over an answer nobody consumed
      ⭐ `A ·` extend check-probe-cards.sh with set-diff checks (a read entry has its stage-doc a-consumer, a claim-serving entry has its 1c line flipped), committing the checker to opening stage docs and the ledger; CC recommends A because the prose-only links are exactly where a false green lives, and the checker already opens targets for the same reason
      `B ·` keep the links prose-enforced and let the venue gate's human read be the only net, committing every round to a manual cross-read of stage docs against 1c
      🛑 `Blocks` nothing; the loop runs either way, which is why the gap is easy to live with and easy to forget
      🤖 `If nobody answers` B, because it is the behavior already in force

### A1 · 📁 The pool: one folder per topic, footnote-numbered
- ⬜ A1.1 · Not started; the drift is recorded in §1.2 and neither document has moved.
- ✅ A1.2 · Already enforced: the checker FAILs any lane line as harvest-owed, and its sidecar pass was removed on 2026-07-18.

### A2 · 🚪 The loop and the one door
- ⬜ A2.1 · Not started; three statements and two answers are recorded in §2.4, and the newest is the description dated 2026-07-20.
- ✅ A2.2 · On the page: §2.2 states the agent, what it may not read, and the no-inline-dispatch rule, each from the worker SKILL.

### A3 · 🧾 What stays behind: the status and the bar
- ⬜ A3.1 · Not started; both triples are in print, recorded in §3.2.

### A4 · 🦷 The teeth: one hard set, and the links without one
- ✅ A4.1 · Superseded on 260817. Insight acceptance and source consumption are checked on the Task/Insight Page; Application checks PageX binding plus Brief/Intervention/Artifact traceability.

### P · 🏁 Page-level
- 🔨 P1 · Written to the rule; a fresh reviewer has not yet read the page against it.

## Files

### ⚙️ Engines · what RUNS this page's subject
- `../../application/haipipe-application/SKILL.md`
  The canonical Application door: it reads settled Insight Pages through PageX and routes missing knowledge to `/haipipe-task insight`.
- `../../task/page-types/haipipe-page-for-insight/SKILL.md`
  The current home of the D→I→K→W evidence contract and the Probe-in/PageX-out boundary.

### 🧪 Checks · what CATCHES a rule breaking
- `../../application/2-phase/1-evidence/haipipe-application-evidence/check-probe-cards.sh`
  The only hard teeth this page names; §4's split of checked against prose-only is read off this file, and option A of the Decision Now row lands here.

### 📋 Contracts · what CARRIES a rule to other pages
- `../../application/haipipe-application/fn/probes.md`
  The application-side paths and verbs every stage reads; it carries the retired pool figure §1.2 records and the DRAFT-authors-①② statement §2.4 records.

### 📥 Input files · what the work READS
- `../PaperSkillBoard-260725/1-QA-design/QA5-the-probe-layer/QA5-the-probe-layer.md`
  QA5@paper, the twin: read for the stake-stripped string, the file-by-path return, and the four vocabulary words this page reuses without restating.

## Glossary

- 🧱 **The wall**: the clean context between an intervention's claim and the bank's evidence; QA5@paper's word, unchanged here.
- 🏦 **The bank**: the project's `tasks/` and `discoveries/` trees, probe-unaware, answering in QA files.
- 🕊 **The collector agent**: `haipipe-probe-q-executor-agent`, the stake-free context that carries a q-executor out and a target path back.
- 🏠 **answered-local**: an entry closed against the intervention's own registries, with no dispatch.
- 🎚 **The settlement bar**: the depth, light or medium or full, that the pinned venue demands of the evidence campaign.

## Law
- 260817 JL · ⚖️ Application owns no Probe. Task/Insight owns evidence work against Task/Discovery; Application consumes settled Insight Pages through PageX.

## Log

260817 · Superseded the Application-local evidence channel and closed the checker-teeth decision as not applicable to the canonical path.
260802 · Created: the application cut of QA5@paper's crossing, with three source drifts recorded (pool shape §1.2, ①② ownership §2.4, status triple §3.2) and the hardening gap put to JL as a Decision Now row.
