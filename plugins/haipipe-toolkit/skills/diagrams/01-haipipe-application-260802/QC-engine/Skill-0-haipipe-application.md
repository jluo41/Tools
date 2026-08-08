# haipipe-application · v0.6.10
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
haipipe-application is a shipped unit: what does it still owe, and is it healthy?

Write here what this unit is for in one paragraph a stranger could follow, why it exists on its own rather than as part of its neighbour, and what would have to be true for it to be considered finished.
The generated sections answer what it IS; only this one can answer whether it is any good.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start a9a78ae25f7ad803 application/haipipe-application -->

```
haipipe-application/
  feedback/
    README.md           63 ln  haipipe-application — Feedback Inbox (orchestrator fallback)
  fn/
    digest.md          145 ln  Digest (condense the session into routed feedback)
    feedback.md        247 ln  Feedback (capture skill feedback, route at capture, fix later)
    probes.md          151 ln  Probe files (application)
  ref/
    render-deck.py     487 ln  Convert a markdown chunk to inline HTML via pandoc (no wrapper).
  CHANGELOG.md         339 ln  haipipe-application — Changelog
  PREFERENCES.md        25 ln  haipipe-application — Behavioral Preferences (portable)
  SKILL.md             359 ln  Skill: haipipe-application (orchestrator)
  stage-strip.sh       115 ln
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start a9a78ae25f7ad803 application/haipipe-application -->

**haipipe-application** · `0.6.10` · last shipped 2026-07-19

- folder   `application/haipipe-application/`
- tools    Bash, Read, Write, Grep, Glob, Skill
- summary  Front door for the intervention lifecycle: parse intent (venue + stage), route to the stage specialists. Each stage runs four phases (draft → probe → revise → check); the intervention RAISES evidence questions as entries in the flat pool 1-probes/, and each stage's PROBE phase binds them to answers in the task/discovery bank through a clean agent — never calling the bank directly. The venue gates which stages fire and how deep claims settle; the 1a–1d ladder (D→I→K→W) is the venue-free evidence spine. History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-application (orchestrator)
==========================================

User-facing entry for the intervention lifecycle. The application lifecycle is a delivery owner: it owns this intervention's story, claims, narrative, displays, artifact text, maturity, and dated work rounds. Project-level evidence lives outside the intervention in discoveries and tasks; when a stage hits a gap, record a delivery need (the Delivery Need Routing section below) and route to the evidence worker.

This orchestrator parses intent and dispatches to stage/specialist skills via `Skill()`. Stage skills internally drive the DPRC phase workers (`2-phase/`); users and this router never invoke phase skills directly. PROBE ends with a VERIFY step (the probe worker's deterministic probe-file checker), and CHECK runs `checks.sh` plus re-runs the probe-file checker as the gate's teeth. Canonical structure: `../README.md` at the application skill root (skill tree, stage-to-procedure map, router rule).

There is no `discover` or `task` verb: reaching the bank is the PROBE phase's job, not the intervention's. A standalone utility question a human wants (a quick lit scan, a data check) goes to the bank's OWN door — `/haipipe-task qa` or `/haipipe-discovery qa` — typed by a person, never proxied by the intervention.

ALWAYS read and honor `PREFERENCES.md` (this skill's own folder): portable, git-tracked global behavioral preferences that survive a machine change. `digest` / `feedback` append flagged global prefs there (merge-or-create).

Verbs
------

One block: verb, aliases and trigger keywords, then where it goes.

```
enter | status | dashboard | preload         -> haipipe-application-enter (open-needs console; GET-OR-CREATE: a missing path offers to scaffold the intervention first; also "enter intervention", "new intervention")
venue | format | modality | channel          -> haipipe-application-venue (recommend + pin; sms/push/reminder/checklist/email/dashboard/ui-card/report all land here; pin writes venue + stages_skipped + claims_settlement into STATUS.md AND produces 0-lifecycle/2-venue/2-venue.md with Artifact Principles — the downstream contract pitch/display/section-edit read)
seed                                         -> haipipe-application-lifecycle seed        (also "opportunity", "why might this work", "kill criteria")
ladder                                       -> haipipe-application-lifecycle ladder      (composite: runs 1a->1d as one sweep with venue-scaled gate batching; also "evidence ladder", "stage 1")
descriptions | describe                      -> haipipe-application-lifecycle descriptions (rung 1a; also "data profile", "how does the data look", "cohort size", "refresh D<n>")
themes | theme                               -> haipipe-application-lifecycle themes      (rung 1b; also "topic space", "what patterns emerge", "thematic")
claims | claim | ledger                      -> haipipe-application-lifecycle claims      (rung 1c; also "what must be true", "what generalizes", "claim gap", "supported", "GAP")
advice | advise | recommendation              -> haipipe-application-lifecycle advice     (rung 1d, the ladder's deliverable; also "design advice", "social norms", "what should the message do", "principles" (legacy))
pitch                                        -> haipipe-application-lifecycle pitch       (also "goal", "one-sentence story", "theory of change")
narrative | arc | structure                  -> haipipe-application-lifecycle narrative
display | elements | panels | widgets        -> haipipe-application-lifecycle display     (also "content plan", "unit jobs" — the retired minimap concern lives here)
section-edit | section | sec | §N            -> haipipe-application-lifecycle section-edit (sectioned venues only)
draft | write | create | generate | make     -> haipipe-application-artifact (compose 0-artifacts/<slug>-v{N}.md from the venue profile + lifecycle stages; "draft the SMS", "make the email")
review | check artifact | compliance         -> haipipe-application-review
claim-audit | verify claims                  -> haipipe-application-claim-audit
deploy | ship | go live                      -> haipipe-application-deploy
round | rounds                               -> haipipe-application-round (dated work rounds; also "todo", "decisions", "applied")
iterate | A/B | performance                  -> haipipe-application-iterate
probe ["<question>"] | probe | probe run [PPNN]  -> the flat probe pool 1-probes/PPNN_<topic>/, one file per TOPIC, one `## QX<n>` ENTRY per q-executor (RAISE a question / SHOW the board / RUN the five-step loop; "run" hands the pool to haipipe-application-probe, the single door to the bank; also "evidence gap", "verify claim", "hypothesis")
feedback "<text>" | feedback list|move       -> fn/feedback.md (resolve BEFORE other parsing)
digest [session] [--dry-run]                 -> fn/digest.md   (resolve BEFORE other parsing)
"<natural language>"                         -> infer via the keywords above, dispatch
```

Examples:

```
/haipipe-application enter "examples/Project-SMSR/applications/interventions/03_refill_reminder"
/haipipe-application venue "timing-aware refill nudge for patients" --no-pin
/haipipe-application claims
/haipipe-application probe "C2: timing matters for refill response"
/haipipe-application probe run PP01
/haipipe-application draft
```

Routing
--------

Resolution order (first match wins):

```
1. feedback / digest first-token             -> run the fn (before any other parsing)
2. first positional matches a verb/alias     -> that target
3. keyword scan over the whole phrase        -> per the trigger keywords in the Verbs block; a named venue/modality anywhere -> venue
4. no args, cwd inside an intervention root  -> enter "."
5. no args, no intervention root             -> chooser (below)
6. input but target unclear                  -> ASK; NEVER silently default a venue (venue gates stages, settlement depth, and artifact shape — expensive to redo)
```

An intervention root is any directory upward containing `STATUS.md`, `0-lifecycle/`, or `0-artifacts/`.

Venue coupling (drives two routing rules): seed + the evidence ladder (1a-descriptions/1b-themes/1c-claims/1d-advice) are venue-FREE; venue pins the modality in STATUS.md between the ladder and pitch (writing `| venue |`, `| stages_skipped |`, and `| claims_settlement |` rows) and writes `0-lifecycle/2-venue/2-venue.md` with Artifact Principles (channel-HOW — distinct from 1d's design advice, content-WHAT); pitch/narrative/display/section-edit are venue-ALIGNED and read those Artifact Principles (consulting `venue/venue-<name>` only for detail beyond them). So: "application" with the ladder gated but no venue pinned -> run `venue` before pitch. Re-targeting ("turn this into a dashboard") -> re-run `venue`; pitch re-couples; the ladder stays unchanged, only its REQUIRED SETTLEMENT deepens or relaxes.

Dispatch notes (only where non-obvious; everything else is `Skill("haipipe-application-<target>")` or `Skill("haipipe-application-lifecycle", args="<verb> ...")`):

```
enter     Path exists -> Skill("haipipe-application-enter", args="<path>"). Path MISSING -> get-or-create:
          CONFIRM FIRST (never create off a typo). Interventions are plain folders (no repo backing):
          scaffold STATUS.md + 0-lifecycle/ + 0-artifacts/ + 1-rounds/ + 1-probes/ under
          the project's applications/interventions/<NN>_<slug>/, then continue straight into the console.
claims    Ladder-virgin guard (JL-agreed thread B, 2026-07-09): if 1a/1b docs are absent, do not
          silently dispatch 1c -- offer the choice: "1a/1b are empty; run `ladder` for the sweep,
          or 1c anyway?" A non-virgin ladder dispatches 1c directly.
probe     Operates on the flat cross-stage pool (1-probes/PPNN_<topic>/; the README board is derived
          from it). "<text>" RAISES a question as a SECTION in the right topic's file, no args SHOWS the
          board, "run [PPNN]" -> Skill("haipipe-application-probe", args="from-buffer <intervention_root> [PPNN]").
          It is the SAME operation at two scopes: this umbrella verb works the WHOLE pool, while a stage's
          PROBE phase works only its own slice -- the sections whose serves: names that stage. Both go
          through the one worker, haipipe-application-probe, which runs the five-step loop MATCH-before-
          DISPATCH and is the ONLY thing that touches the bank. A claim's status lands in 1c-claims.md,
          never in a probe file. Anatomy + model: fn/probes.md.
```

After dispatch, capture the specialist's structured tail (status / summary / artifacts / next) and present it.

Closing Block (end every reply)
--------------------------------

THE single source of truth for the closing block and the focus strip in application sessions (mirrors paper's Closing Block; every stage / enter skill inherits this section). In an intervention session, END every reply with ONE fenced `text` block: a titled top rule carrying `🎯 application · <active-stage> 🔥`, a two-line simplified tail, a plain bottom rule, then the TWO-LINE focus strip (stage + phase):

```text
── 🎯 application · claims 🔥 ─────────────────
status:  ok · claims            (status and active stage merged on one line; intervention_root dropped)
next:    <single recommended command>
──────────────────────────────────────────────
stage:   seed ✅  descriptions ✅  themes ✅  claims 🔥🚀  advice ⬜  venue ⬜  pitch ⬜  narrative --  display --  section-edit --  →  draft ⬜  →  review ⬜  →  deploy ⬜
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

Markers: 🔥 active now (what this session works on) · 🚀 frontier (farthest the intervention has ever reached) · ✅ done (Gate-Ledger-approved; venue slot: pinned) · ⬜ not started · `--` skipped by the pinned venue. Rules: EXACTLY one 🔥 and EXACTLY one 🚀 per line, never zero -- "reached" means entered, not completed, so a virgin intervention working its first phase renders `draft 🔥🚀`; they split only on loopback (the frontier slot keeps 🚀 while 🔥 moves back) and collapse to `🔥🚀` when they land on the same slot; the phase line always describes the 🔥 stage's DPRC phases. Venue-skipped stages render `--` and can never carry 🔥 or 🚀.

Render the stage line DETERMINISTICALLY with the helper (never hand-type it; it drifts): `sh "${CLAUDE_SKILL_DIR:-.}/stage-strip.sh" <intervention-dir> [<session-stage>]` (the script lives IN this skill folder, next to this spec; it reads `| current_layer |`, `| venue |`, `| stages_skipped |`, and the Gate Ledger from STATUS.md). The phase line is rendered by the 🔥 stage's skill from its own DPRC progress.

Gate-aware: advancing `current_layer` requires an EXPLICIT approval action that the current stage is done (the Stage Gate Protocol section below) -- by the human (copilot mode) or by the check worker's persona standing in (autopilot/unattended modes); once STATUS.md carries the gate ledger, ✅ means "approved", and the ledger records who approved.

Stage Gate Protocol
--------------------

THE single source of truth for stage gates across the application family (every stage / phase skill inherits this section). A stage is only "done" when it is EXPLICITLY approved. The system must never auto-advance. This is the user-control mechanism for the intervention lifecycle. Application rewrite of the paper family's gate protocol; the venue scales the gate's DEPTH, never its existence.

**Gate protocol (per-stage loop)**

1. **Produce** the stage artifact through DRAFT → PROBE → REVISE (`../2-phase/` workers). The PROBE phase ends with a VERIFY step: `check-probe-cards.sh` FAILs cards left `planned|dispatched|failed`, dangling refs, and `harvest: OWED` lane debts.
2. **Present exit criteria** with per-item check/fail marks (per-stage table: `../2-phase/3-check/haipipe-application-check/SKILL.md`).
3. **ASK** "Stage <X> looks ready -- confirm to close and move to <next>?"
4. Only on **explicit approval**: write the Gate Ledger row and update STATUS.md `current_layer` to the next non-skipped stage.

The system **STOPS at step 3 and WAITS**. No next-stage work until approved.

**Venue-scaled depth**

```
simple venues (sms/push/reminder)      INLINE gate: exit criteria as one short
                                       checklist in the reply; user's "ok" approves
medium venues (checklist/email)        INLINE by default; full report on request
complex venues (dashboard/ui-card/     FULL gate: complete CHECK report (criteria +
report)                                evidence spot-checks + flags) before the ask
```

Depth changes the REPORT, not the rule: every stage still ends with an explicit approval and a ledger row.

**Ladder gate batching (stage-1 family)**

The evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice) batches its gates by venue depth -- approval is batched, never skipped, and every rung still gets its own ledger row:

```
light    ONE combined inline gate at 1d covering all four rungs;
         one approval writes four ledger rows
medium   combined gate at 1c (covers 1a-1c) + own gate at 1d
full     four individual gates, one per rung
```

Venue unpinned (the normal case -- the ladder is venue-FREE and runs before the pin): apply `light` batching provisionally; a later pin to a deeper venue re-opens only the GATE (re-present criteria at the deeper bar), not the content.

Within the ladder, a rung's CHECK routes like any gate: **approve** advances to the next rung (1c → 1d); **revise** reruns the same rung; upstream symptoms **loop back** (1c → 1a for stale/missing data, 1c → 1b for a wrong theme) per the loopback rule. Whatever the batching, the ladder EXITS to venue only through the 1d gate.

**Rounds within a rung (the breadth/depth contract)**

REVISE ends with a self-assessment -- did this round surface anything new? If yes, another DRAFT->PROBE->REVISE lap runs BEFORE CHECK (`[ROUND n]` in the rung's `_LOG`); CHECK fires only when a round comes up dry. Venue-scaled round depth: light -- one round suffices unless the rung self-assesses a blocker; medium -- loop-until-dry on 1c; full -- loop-until-dry on every rung. Mid-phase back-routing (`[ROUTE -> <rung>]`) files the upstream slot/card immediately and never waits for a gate -- rounds are internal; only CHECK involves the user. And the gate itself is a lens: at a GROW-loop rung's CHECK the user is asked which data topics are still missing; a `grow` verdict converts the answers to new slots + planned probes and re-opens DRAFT as [ROUND n+1] -- approve means saturated AND the user added nothing.

**Mechanical teeth**

The gate is not prose-only. Before the ask, the check worker (`../2-phase/3-check/haipipe-application-check`) runs two deterministic checkers, and any FAIL blocks the gate from going green:

- `check-probe-cards.sh` (re-run of the probe worker's VERIFY step): a `status: planned` card or a `harvest: OWED` lane at the gate means a probe that never ran — FAIL.
- `checks.sh` (markdown-safe deterministic checks): em-dash (❌ house rule), AI-voice tells, TODO/FIXME, bibtex-in-markdown.

Findings are seeded as `> CHECK:` threads in the STAGE DOCS only; `0-artifacts/*.md` stay clean because the artifact IS the deliverable text — artifact-level findings go to the Gate Ledger `Notes` column instead.

**Confirmation Ledger in STATUS.md**

STATUS.md carries a **Gate Ledger** -- one row per stage:

    | Stage | Confirmed | Date | By | Notes |
    |-------|-----------|------|----|-------|
    | seed | yes | 2026-07-06 | JL | kill criteria set |
    | claims | yes | 2026-07-06 | JL | settlement: light met |
    | pitch | no | -- | -- | -- |

`By` records who approved: the human (copilot mode, the default) or `persona:<preset>` (unattended runs only -- attendance modes and persona presets live with the check worker). The stage strip's ✅ means "confirmed in the ledger", NOT "artifact exists on disk". A stage with a doc but no ledger row is unconfirmed. Venue-skipped stages never get ledger rows (they render `--` in the strip).

**Autonomy policy**

- **Stage TRANSITION** = always PAUSE (ask before advancing).
- **Work WITHIN a stage** = can be autonomous (read, draft, raise `state: planned` probe sections, backfill).
- **Taste-bearing choices** (framing, emphasis, scope, venue pick) = PAUSE to elicit.
- **Mechanical formatting** = autonomous.
- **Evidence dispatch** = the PROBE phase worker is the only door; a stage never reads discoveries/, tasks/, or legacy probes/ inline, and never dispatches discovery/task orchestrator agents itself.

**Recovery**

If an intervention reached a late stage without per-stage confirmations, the gate state is UNCONFIRMED for all stages. A re-walk resets to seed and confirms each non-skipped stage one-by-one. Artifacts on disk are NOT deleted -- only the gate state resets.

No-Arg Chooser
---------------

When no intervention root is found, do not fan out. Emit a compact chooser (one line per entry; the Verbs block carries the detail):

```
🎯 haipipe-application: no intervention detected. Pick an entry:
  venue       /haipipe-application venue "<topic or intervention-path>" [--no-pin]
  enter       /haipipe-application enter "<intervention-path>"   (missing path -> offers to scaffold it)
  draft | probe    (see /haipipe-application help text above)
```

Specialist Return Contract
---------------------------

Each specialist returns a tail block:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what the specialist did
artifacts: [paths created, read, or modified]
next:      suggested next command
```

Delivery Need Routing
----------------------

THE single source of truth for how an intervention (message / checklist / dashboard / report) records an evidence gap as a QUESTION, routes it to the bank, and backfills when the answer returns. Application-owned; the paper family keeps its own copy. There is no cross-skill shared file. The model itself belongs to `probe` (`../../probe/haipipe-probe/SKILL.md`); this section is the application-side routing.

Application work is demand-driven: a claim, content element, artifact slot, or round todo may reveal that the next action is evidence work. The enter/status path surfaces those needs before recommending more drafting.

**How the application talks to the bank**

A need is a QUESTION the intervention cannot answer itself. It is RAISED as a `Q-<Stage>-<n>` in the stage doc's Q-consumer section — which is where its STAKE lives — and bound to the bank by an ENTRY in the flat probe pool `1-probes/PPNN_<topic>/`. No message bus, no shared contract file. Two channels carry it, and the agent (this session) is the medium:

```
1. Command   a stage's DRAFT raises the questions (the Q-consumer list) AND authors
             their probe plan (① ORGANIZE + ② MATCH); APPROVE (human) reviews draft +
             plan together and picks which to pursue. `/haipipe-application probe run
             [PPNN]` hands the approved set to haipipe-application-probe (the PROBE
             phase worker), which runs that plan FORWARD — ③ DISPATCH → ④ POINT →
             ⑤ INTERPRET — and never re-matches. DISPATCH goes through the stake-free
             collector Agent(haipipe-probe-q-executor-agent) — it calls the
             task/discovery orchestrators in clean context. Stages never call an
             orchestrator directly.
2. Disk      the question lives as an ENTRY (`## QX<n>`) in 1-probes/PPNN_<topic>/;
   (async)   its **target**: binds by PATH to a QA file the executor wrote in the bank.
             The entry's `### a-executor` holds a COPY of that QA answer; each
             Q-consumer then writes its own a-consumer (its `Answer:` line in the stage
             doc, anchored `[source: PP<NN>]`) in the intervention's words, and the
             application reads THAT to backfill. No handshake, just read/write the same
             entry in turn.
```

Who owns which format: the application owns the QUESTION — the STAKE stays in the stage-doc Q-consumer, and the probe entry carries only the stake-free `### q-executor`, the one thing the bank ever sees. The bank owns the ANSWER (the QA file's `## Answer`, in general language). A probe is COMMUNICATION, not judgment — it carries a question out and an answer back, and nothing else. A CLAIM's status is written by the author into `1c-claims.md`, never in the probe file.

**When to raise a question**

Only when the deliverable requires EVIDENCE the project does not yet have. A framing/format/tone problem stays inside the application lifecycle. An evidence gap becomes a question bound to the bank.

```
stage gap -> a Q-consumer in the stage doc + an ENTRY in 1-probes/ (DRAFT: ① ORGANIZE + ② MATCH)
          -> haipipe-application-probe runs it forward (③ DISPATCH -> ④ POINT -> ⑤ INTERPRET)
          -> collector -> QA file answer -> ### a-executor -> each a-consumer
          -> 1c-claims status backfill
```

**Routes**

```
claim needs evidence / robustness / literature / a data artifact  -> /haipipe-application probe "<question>"  (a SECTION in 1-probes/; MATCH first, dispatch only what MATCH cannot close)
outside context / benchmark (non-claim)                          -> /haipipe-discovery <question>
display element needs materialized output (not claim-gated)      -> /haipipe-task-for-display <need>  (or /haipipe-task <contract>)
wording/structure/tone                                           -> the owning lifecycle stage skill (audience profile shapes tone)
standalone utility (a HUMAN, not the intervention: lit scan, data check) -> /haipipe-task qa | /haipipe-discovery qa (the bank's own door)
```

Claim-related evidence goes through a stage's PROBE phase — the entry preserves the claim-evidence chain and makes the backlog visible. Non-claim utility work goes straight to the task/discovery door; if the answer later matters, open an entry whose `**target**:` points at the already-written QA file (`bank: reuse` — nothing re-runs).

**Question record**

Each open question is one ENTRY in `1-probes/PPNN_<topic>/` (anatomy + states: `fn/probes.md` and `../../probe/haipipe-probe/SKILL.md`). One file per TOPIC; one `## QX<n>` entry per Q-EXECUTOR, each with four `###` subsections — the file is Q-executor-oriented, and the consumers hang off it:

```
## QX<n>          one entry per Q-EXECUTOR; a topic-local id
### q-executor    the question in general language, stake stripped — the ONLY thing sent to
                  the bank, FROZEN; carries its own Deliverable: and Accepted: lines
### q-consumer    one bullet per consumer this q-executor serves:
                  * Q-<Stage>-<n> — <that consumer's ORIGINAL question, copied in>
### bank binding  **route**:  task | discovery          the dispatch door, AUTHORITATIVE
                  **bank**:   reuse | run | code | new  the PROBE ② verdict on what the bank needs
                  **target**: a PATH to the answering QA file (`NEW <path>` while it does not exist)
                  **state**:  planned | commissioned | answered | read | answered-local | failed
                              (DERIVED from disk)
### a-executor    a COPY of the answering QA file's answer, written at harvest
```

The STAKE lives in each Q-consumer, in the stage doc, and is NEVER sent to an executor; a claim's status lives in `1c-claims.md`, written by the author. BUILD-lane entries (days-to-weeks work) additionally carry `**owner**:` · `**eta**:` · `**blocks**:` · `**cross-project**:` under `### bank binding`, present only at `state: commissioned`.

**Backfill (the return direction)**

When the QA file lands, ⑤ INTERPRET copies its answer into the entry's `### a-executor`; backfill flows FROM there:

```
- write `### a-executor` (a copy of the QA answer, anchored to **target**), ONLY against
  an answered, non-superseded target — `1-probes/` is the consumer-side single source of truth
- each Q-consumer then writes its OWN a-consumer in the stage doc (its `Answer:` line,
  station ②, anchored `[source: PP<NN>]`) — the answer in the intervention's own words
- if a Q-consumer serves a claim, the AUTHOR flips that claim's STATUS in 1c-claims.md
  (supported | weak | GAP), flipping the C-line AND its Evidence Campaign row — never in
  the probe file; keep the overclaim check (never causal from associational evidence)
- refuted / GAP evidence: drop or reword (never ship an unsupported claim); a weak/GAP
  claim stays with the caveat recorded, and the venue gate reads the campaign against its bar
- the bank NEVER edits application files; the executor writes the QA file, the worker
  harvests it, the application decides how to phrase it for its audience
```

The same landed QA answer can serve both a paper and an application; each reads the same file differently and frames it for its own audience.

ALL evidence enters through a stage's PROBE phase; the intervention never calls the bank directly. Resolved evidence backfills into the ladder rungs (`1a-descriptions` numbers, `1c-claims` statuses), `4-display`, sections, or round logs. Evidence workers never own the intervention story.

Structure Pointers
-------------------

Each area's internal contract lives with its owner; consult, never restate:

```
skill tree (0-enter / 1-lifecycle / 2-phase / 3-deliver / 4-iterate)
                                   -> ../README.md (skill root; Skill Structure + Stage to Procedure + Router Rule)
intervention-folder layout         -> ../README.md (skill root) + ../1-lifecycle/haipipe-application-lifecycle/SKILL.md (Folder Contract)
lifecycle stages + venue gating    -> ../1-lifecycle/haipipe-application-lifecycle/SKILL.md (Intervention Lifecycle Contract)
stage gates + Gate Ledger          -> this file, Stage Gate Protocol section
delivery needs + probe interface   -> this file, Delivery Need Routing section
rounds                             -> 0-enter/haipipe-application-round (same vYYMMDD contract as paper)
venue knowledge (structure + tone-by-audience)  -> ../venue/venue-<name> packs (venue is knowledge, not a pipeline)
```

Composing with Evidence Workers
--------------------------------

```
/haipipe-application (router)
        ├─► /haipipe-application-lifecycle   (seed -> 1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice -> [venue] -> pitch -> narrative° -> display° -> section-edit°)
        ├─► /haipipe-application-artifact    (draft the deliverable from the venue profile + lifecycle stages)
        │
        │   evidence path (a claim hits a gap):
        └─► questions RAISED as entries in 1-probes/PPNN_<topic>/  ─►  haipipe-application-probe (the PROBE phase worker)
                                            └─► Agent(haipipe-probe-q-executor-agent)  (stake-free collector; dispatches /haipipe-task + /haipipe-discovery)
                                                 └── answers land as QA files; the a-consumer + 1c-claims status backfill into the ladder, sections, round logs

        a stage reaches the bank ONLY through its PROBE phase — no direct discover/task verb
```

Feedback & Digest
------------------

`/haipipe-application feedback "<text>"` captures a complaint/wish about THIS skill family, capture-time-routed into the concerned sub-skill's `feedback/` inbox (folder = the record; orchestrator inbox is the fallback), MERGE-OR-CREATE so inboxes stay self-limiting; `feedback list [skill]` aggregates, `feedback move <file> <skill>` re-routes. `/haipipe-application digest [session] [--dry-run]` harvests a session transcript into discrete feedback items (dedup, mandatory confirm gate, then the same capture; global behavioral prefs fan out to every orchestrator's PREFERENCES.md instead of the inboxes). Full spec: `fn/feedback.md` + `fn/digest.md`; this section is a pointer, not the spec.

### The other files

7 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
PREFERENCES.md          25 ln  haipipe-application — Behavioral Preferences (portable)
feedback/README.md      63 ln  haipipe-application — Feedback Inbox (orchestrator fallback)
fn/digest.md           145 ln  Digest (condense the session into routed feedback)
fn/feedback.md         247 ln  Feedback (capture skill feedback, route at capture, fix later)
fn/probes.md           151 ln  Probe files (application)
ref/render-deck.py     487 ln  Convert a markdown chunk to inline HTML via pandoc (no wrapper).
stage-strip.sh         115 ln
```

<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated 260802 1200; nothing ruled yet.

## Log
260802 1200 · page generated from `application/haipipe-application/` by `skillpage.py new`

<!-- haipipe:skill:log:start a9a78ae25f7ad803 application/haipipe-application -->

Converted from the skill's own `CHANGELOG.md`: 22 releases.

260724 · `0.6.10`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 6.10.0; older entries below keep their original numbers).
260719 · `6.10.0`
      - ⑨ TOMBSTONES erased. Owner ruling (JL): "不需要留退役告示,直接抹除任何痕迹" — a doc states the CURRENT contract and never names the dead thing.
        `fn/probes.md`: the 💀 ban-list on retired state words becomes "An entry in flight is `commissioned`";
        `SKILL.md:300`'s "There is NO `## Why` / NO `## Verdict` / NO G1-G2-G3" becomes the positive statement of
        where the stake and the claim status actually live.
      - ⑩ probe files hold `## QX<n>` ENTRIES, not "sections" — wording corrected in the description, summary, the router line, and the evidence-path diagram.
260719 · `6.9.0`
      - Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
        "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
        each site now names either `probe` or the actual path.
        Touched: SKILL.md (Delivery Need Routing model pointer, probe-entry anatomy pointer) and `fn/probes.md`
        (the MODEL-owner line, the full-spec pointer).
      - No `a-consumer` change here: every occurrence in this skill is the LIVE stage-doc concept (station 2).
260531 · `1.0.0`
      - baseline.
260622 · `2.0.0`
      - restructured around intervention lifecycle.
260623 · `3.0.0`
      - rename stages to paper vocabulary; add venue; venue-driven stage requirements.
260623 · `4.0.0`
      - remove format specialists (message/ui/report) — absorbed into venue profiles; remove context + plan skills — absorbed into lifecycle orchestrator and claims stage; single draft skill reads venue profile.
260706 · `5.0.0`
      - FAMILY ROLLUP: claims-before-venue spine (R1); minimap retired into display, section-edit venue-gated (R2); ask retired to _archive/, enter console is the entry (R3); full DPRC 2-phase/ bucket — draft/probe/revise workers NEW, gate renamed check (R4). Folderless probe adopted: per-stage _PROBE/PPNN cards + 1-probe-plans/README.md index, plan-from-need + confirmed enum retired. Buckets renumbered 0-enter/1-lifecycle/2-phase/3-build-deploy/4-iterate; a shared wiki bucket replaced both ref/ homes (that bucket itself retired 2026-07-19, its docs folded into the owning skills); root README+PHILOSOPHY added; Closing Block + venue-aware stage-strip.sh added; draft skill renamed haipipe-application-artifact (paper-alignment refactor; executed SOP archived below).
260707 · `5.1.0`
      - FAMILY ROLLUP (paper-alignment round 2, porting paper b2c5a23 enforcement): probe worker 2.0.0 gains STEP 4 VERIFY (check-probe-cards.sh fork) + PROOF 1-4 blocks + venue-scaled `harvest: OWED` lane debts (_VALUES_ always, _CITATION_ sectioned venues only, _DISPLAY_ only with display units) + ref/ dispatch tables; check worker 4.0.0 gains gate wiring (card-checker FAIL blocks green) + markdown-safe checks.sh (em-dash, AI-voice tells, TODO/FIXME, bibtex-in-md) + `> CHECK:` seeding in stage docs only, artifact findings → Gate Ledger notes (R2c, JL ruled 2026-07-07); draft 1.1.0 gains WebSearch/WebFetch as DRAFT-only orientation fuel — "DRAFT may search; PROBE must dispatch"; seed 3.2.0 narrows probe scope to feasibility + registers [FORWARD → CLAIMS] pointers in _LOG_0-seed.md, claims 5.1.0 DRAFT consumes them (unconsumed pointer fails claims CHECK); PREFERENCES.md gains the family-generic real-probe entry + the paper-drift alignment-watch line (R6); 2-phase/ gains thin USAGE.md + WIRING.md + the ONE-pipeline/HARVEST note in README.md; router SKILL.md + wiki 03/06/08 one-line mentions. Round-2 SOP archives below on close-out (same convention as round 1).
      Archived SOP — paper-alignment refactor (2026-07-06, executed; archived 2026-07-07)
      -----------------------------------------------------------------------------------
      Condensed from the executed SOP-paper-alignment.md (deleted per its own close-out step; full text recoverable from git history at Tools 0364482).
      - **Target**: application becomes paper's structural twin — same spine order (claims before venue), same venue-FREE/venue-ALIGNED coupling, same DPRC phase workers, same folderless probe door, same console/strip/gate machinery — differing ONLY in declared deltas (deliverable = venue artifact not manuscript; _audience/ axis; venue-gated stage skipping; claims settlement depth; deploy/iterate tail).
      - **Decision record (JL 2026-07-06)**: R1 spine reorder APPROVED (claims venue-FREE, settlement depth becomes a gate read, slot-mapping moves venue-side); R2 minimap RETIRES into display per-unit contracts, section-edit venue-gated; R3 ask RETIRES to _archive/ (entry = enter console; ad-hoc questions = /haipipe-probe direct ask); R4 FULL 2-phase/ DPRC parity (gate → 3-check rename, persona/attendance kept; ONE revise worker, paper's content/humanizer/results split deferred; probe worker mirrors paper's BOOKKEEP → DISPATCH → TRANSLATE).
      - **Commits (Tools main, post-rebase ids)**: fca4bc8 structure moves · 10e8aef load-bearing rewrites · a5c1659 peripheral sweep · 1659aa7 ask-residue close-out · 0e37e0d + a7446b6 three bench-found stage-strip.sh bugs (both families) · f330280 phase-3 port of paper 765696f (evidence-campaign claims 5.0.0, venue 3.0.0 stage doc, _EVIDENCE_ → _VALUES_) + 11 audit fixes from an 18-agent adversarial-verify workflow.
      - **Bench exams (both PASSED, JL approved 2026-07-06)**: light path examples/ProjApp-SMSDesign/applications/03_bench_refill_timing_sms (seed→claims→venue→pitch→draft; fresh light probe, 18 verified sources, round-1 fabrication caught+rebuilt; strip renders `--` on skipped stages) · full path 04_bench_timing_report (all stages incl. section-edit; reused full probe → G1/G2/G3 verdict in PPNN card ## Verdict + campaign flip + _VALUES_; report assembled from 0-sections/).
      - **Execution notes**: data-contract-schema.md archived with ask (data/contract.yaml stays in the intervention schema); gate-persona.md + attendance-modes.md kept with the check worker (SESSION_STATE plumbing → flag/Gate-Ledger wiring); fn/digest.md "even if confirmed" untouched (digest confirm-gate semantics, not the verdict enum); latent paper-side stage-strip greedy-sed bug found+fixed while adapting; 7 dangling pre-v4 .claude/skills/haipipe-application-* symlinks removed workspace-side.
      - **Deliberately unchanged**: _venue/ + _audience/ pack structure; 0-artifacts/ naming; PPNN numbering + _PROBE/ + 1-probe-plans/README.md index names; probe/discovery/task/insight layer contracts; legacy applications/ask/ + existing intervention folders = dead history, no migration.
260709 · `6.0.0`
      - FAMILY ROLLUP (ladder restage; SOP-ladder-restage.md at the family root archives here on close-out): stage 1 split into the venue-FREE EVIDENCE LADDER `1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles`, echoing D->I->K->W without reusing the insight-KB letter names (JL rulings 2026-07-09: "claims are not the things we want to get the experiment dataset"; Descriptions/Themes/Claims/Principles "sounds like D, I, K, W"; paper delivers K, application delivers W — the artifact carries no D/I body and lives on dynamic data, so application climbs one more rung than paper).
      - NEW rung skills: haipipe-application-descriptions 1.0.0 (anchored data summaries + as-of dates, FORWARD consumer, staleness stamp duty), haipipe-application-themes 1.0.0 (grounded thematic extraction), haipipe-application-principles 1.0.0 (P<-C directives, W-actionability test, on-request W deposit, ladder gate host); claims 6.0.0 slimmed to rung 1c (folder git-mv'd 1-claims/ -> 1c-claims/; theme tags; FORWARD reader moved out).
      - Ladder mechanics: ladder-local id chain P<-C<-T<-D mandatory (R2); `[STALE <id> refreshed <date>]` staleness propagation from 1a refreshes, CHECK fails on unresolved tags (R3); venue-scaled GATE BATCHING — light: one combined gate at 1d writing four ledger rows, medium: 1c+1d, full: four (R6, the Stage Gate Protocol); insights downgraded to optional deposit — judgment lives in PP-card verdicts (R7); `_VALUES_` stays with 1c, the 1a doc IS the anchored-numbers doc (R8); downstream readers (pitch/narrative/display/section-edit/venue/artifact/review/claim-audit) now read 1d-principles as primary input with 1c-claims as evidence backstop, claim-audit traces artifact -> P -> C -> anchor (R9).
      - Wiring: router 6.0.0 (verbs descriptions/themes/principles + composite `ladder`), lifecycle orchestrator 4.0.0, stage-strip.sh keys + `1a-` prefix normalization (tested: frontier collapse + loopback split render correctly), probe ref/per-stage-dispatch 1a-1d rows, check worker per-rung exit criteria + argument-hint, seed FORWARD consumer note + handoff -> ladder, iterate Step 4 backfills fresh A/B numbers into 1a BEFORE triage, enter console read-order/diagnosis/maturity/needs/loopback, wiki 03/05/06/08, PHILOSOPHY + README (delta table + retired-names rows), fn/probe-plans + fn/feedback paths, PREFERENCES alignment-watch ladder caveat (ports map paper claims-stage changes onto 1c, never re-converge).
      - Migration: legacy interventions rename `0-lifecycle/1-claims/` -> `0-lifecycle/1c-claims/` (+ create sibling rung folders) on next open; skills do not dual-read old layouts. Live bench exam (SOP §8) pending on the next real intervention.
      - Templates (JL follow-up, same session: "no ref/ no template ... what the stage generated markdown looks like"): every 1-lifecycle stage skill gains `ref/<stage>-template.md` (seed, descriptions, themes, claims, principles, pitch, narrative, display, venue — 9 files, paper convention), each SKILL.md gains a canonical-template pointer line, and draft worker 1.2.0 gains the template registry table (WRITE reads the stage's template; the worker carries none of its own).
260709 · `6.1.0`
      - FAMILY ROLLUP (walkthrough rulings + advice rename, same session as 6.0.0): rung 1d RENAMED principles -> ADVICE (haipipe-application-advice 1.1.0; JL: advice is counsel downstream stages adopt or decline — declined entries persist; also kills the principles-vs-Artifact-Principles double-use). Ids P<n> -> A<n>, maturity `principled` -> `advised`, verbs advice|advise|recommendation (+ legacy principles alias), full-tree sweep (router, lifecycle, strip keys, wikis 03/05/06/08, enter, draft registry, check criteria, fn maps, downstream readers, templates).
      - Other executed rulings: display units D<nn> -> U<nn> + all four inline schema blocks converted to ascii ====/---- (JL heading ruling); P/A status enum drops `stale` (staleness = the [STALE] tag alone); router gains the ladder-virgin guard on bare `claims`; the Stage Gate Protocol codifies the ladder routing invariant (rung CHECK: approve advances / revise reruns / loopback upstream; exit to venue ONLY via the 1d gate) + gate depths parked for the bench.
      - Cumulative DIKW reading adopted as canon (descriptions=D, themes=D+I, claims=D+I+K, advice=D+I+K+W — each rung CONTAINS its lower layers). Round-2 candidates recorded in SOP-ladder-restage.md §10: explore|exploit role tags, 2-design stage + venue-design-doc pack, per-rung maturity.
      - Resolved/parked `> JL:` / `> CC:` walkthrough threads archived below verbatim and removed from the working files (paper-family comment-lifecycle convention); OPEN threads stay in-file awaiting `> USER:` — 1d derivation bars + explore|exploit proposal (1d-advice SKILL.md) and maturity vocab data-described/advised (the README Skill Structure section).
      Archived comment threads — ladder walkthrough (2026-07-09, verbatim)
      ----------------------------------------------------------------------
      Resolved/parked `> CC:` / `> JL:` threads from the 6.0.0-6.1.0 walkthrough, moved here so the working files stay clean (paper-family comment-lifecycle convention). OPEN threads still live in-file awaiting `> USER:`: 1d derivation bars + explore|exploit proposal (1d-advice SKILL.md) and maturity vocab data-described/advised (the README Skill Structure section).
      **@ 1-lifecycle/0-seed/haipipe-application-seed/SKILL.md — schema-block heading style (PRIMARY thread; one ruling covered seed/pitch/narrative/display)**
      > CC: 🎨 PRIMARY THREAD (one ruling covers seed / pitch / narrative / display): the inline schema blocks use `#`/`##` headings while each skill's formatting rule + its ref/<stage>-template.md are ascii (`=====`/`-----`).
      >
      >             SKILL.md                        ref/<stage>-template.md
      >     +------------------------+            +------------------------+
      >     | 📄 inline schema block |            | 📄 canonical template  |
      >     |    #/## headings ⚡    |     vs     |    ascii =====/-----   |
      >     |    full placeholders   |            |    full placeholders   |
      >     +------------------------+            +------------------------+
      >          └── ⑥ 复述漂移: same format stated 2×, edits WILL diverge ──┘
      >
      >     A    rewrite the 4 illustration blocks to ascii (consistent, keeps the duplication)
      >     B    bless as "example-only" with a one-line note (cheapest, drift stays possible)
      >     C ✅ shrink each inline schema to a section-NAME skeleton + "full form: ref/<stage>-template.md" (single source of truth — kills the drift class the skillset reviews hunt as ⑥)
      >
      > CC: my rec = C. Reply `> USER:` below; I will apply the same ruling to all four files.
      > JL (via the display-file thread): heading use "---" and "====" styles.
      > CC: ✅ executed as A per that ruling — all four illustration blocks converted to ascii, mirroring each ref/<stage>-template.md.
      **@ 1-lifecycle/2-pitch/haipipe-application-pitch/SKILL.md — heading-style pointer stub (resolved at the seed thread)**
      > CC: 🎨 heading-style thread — the schema block below uses `#`/`##` vs the declared ascii rule; ONE ruling covers seed/pitch/narrative/display. Full options + diagram live in `1-lifecycle/0-seed/haipipe-application-seed/SKILL.md` (reply there).
      **@ 1-lifecycle/3-narrative/haipipe-application-narrative/SKILL.md — heading-style pointer stub (resolved at the seed thread)**
      > CC: 🎨 heading-style thread — the schema blocks below use `#`/`##` vs the declared ascii rule; ONE ruling covers seed/pitch/narrative/display. Full options + diagram live in `1-lifecycle/0-seed/haipipe-application-seed/SKILL.md` (reply there).
      **@ 1-lifecycle/4-display/haipipe-application-display/SKILL.md — display-unit id collision D01 -> U<nn> + local heading-style ruling**
      > CC: 🆔 id collision needs your ruling — the illustration below names display units `D01/D02`, but `D<n>` now belongs to 1a description ids (ladder restage).
      >
      >     🆔 id namespaces after the restage
      >       1a-descriptions        1b       1c       1d        4-display
      >     +-----------------+   +------+ +------+ +------+  +----------------+
      >     | 📊 DS<n> dataset |   | 🧩 T |▶| 🧾 C |▶| 🎯 P |  | 🖼️ units:      |
      >     | 📈 D<n>  entry   |──▶+------+ +------+ +------+  |  SKILL: D01 ⚡ |
      >     +-----------------+                                |  ref/:  U01 ✅ |
      >             ▲                                          +----------------+
      >             └──────── ⚡ two meanings of "D" ──────────────────┘
      >
      >     A ✅ rename display units to U<nn> (template already does; 1 schema block to fix; no filled display docs exist yet)
      >     B    rename 1a entries instead (e.g. A<n>; re-edits 5 fresh files + SOP; loses the D-rung DIKW echo)
      >     C    keep both namespaces (zero cost now, but claim-audit greps D<n> cross-rung and will misfire)
      >
      > CC: my rec = A. Reply `> USER:` below.
      > JL: Yes, I agree. please go ahead.
      > CC: ✅ done — units renamed to U<nn> and the blocks below converted to ascii per your heading ruling; they now mirror ref/display-template.md.
      > CC: 🎨 heading-style: ONE ruling covers seed/pitch/narrative/display; the full options thread lives in `1-lifecycle/0-seed/haipipe-application-seed/SKILL.md`.
      > JL: heading use "---" and "====" styles.
      > CC: ✅ applied to THIS file's blocks below; if this ruling is global (ascii illustrations in all four SKILLs), confirm at the seed thread and I'll sweep pitch/narrative too.
      **@ 1-lifecycle/1a-descriptions/haipipe-application-descriptions/SKILL.md — [FORWARD -> CLAIMS] token kept verbatim**
      > CC: 🏷️ token ruling needed — `[FORWARD -> CLAIMS]` is kept VERBATIM (SOP R5) even though this rung (1a) now consumes it.
      >
      >     🌱 seed _LOG                        🪜 ladder
      >     +------------------------+  consume  +--------------------------+
      >     | [FORWARD -> CLAIMS] 🏷️ | ────────▶ | 1a DRAFT routes each:    |
      >     | PPNN_<slug>            |           |  📊 data need → 1a plan  |
      >     +------------------------+           |  🧾 verdict   → 1c PP    |
      >             ▲                            +--------------------------+
      >        📄 paper twin writes the SAME token (its consumer IS claims)
      >
      >     A ✅ keep [FORWARD -> CLAIMS]: grep-stable AND identical to paper's token, so alignment-watch ports stay 1:1; name lies slightly (consumer is 1a, documented here)
      >     B    rename [FORWARD -> LADDER]: accurate, but diverges from paper + old interventions need a sed at migration
      >     C    write new token, read both: smooth but two tokens forever = drift bait
      >
      > CC: my rec = A (paper-twin symmetry outweighs naming purity). Reply `> USER:` below.
      > JL: ok, I agree.
      > CC: ✅ resolved — token stays `[FORWARD -> CLAIMS]`; no file changes needed.
      **@ 1-lifecycle/1d-advice/haipipe-application-advice/SKILL.md — status enum drops `stale` (staleness = [STALE] tag alone)**
      > CC: 🏷️ status vocabulary `active | caveated | stale` was CC-invented — and while diagramming this I noticed a redundancy worth fixing:
      >
      >     status: stale 🏷️            [STALE D3 refreshed 07-09] 🏷️
      >     (entry header field)  ⚡ vs   (mechanical tag, checker-enforced)
      >          └──── two mechanisms for ONE concept = drift bait ────┘
      >
      >     A    keep active | caveated | stale (as shipped)
      >     C ✅ drop `stale` from the enum → `active | caveated`; staleness lives SOLELY in the [STALE] tag (one mechanism, already checker-enforced)
      >
      > CC: my rec = C (improves on my own draft; the status copy would rot). Reply `> USER:` below.
      > JL: I agree.
      > CC: ✅ done — enum is now `active | caveated` in ref/advice-template.md; staleness lives solely in the [STALE] tag.
      **@ haipipe-application/SKILL.md — bare `claims` verb: ladder-virgin soft redirect**
      > CC: 🗣️ verb ruling — bare `claims` now routes to rung 1c ONLY; the full 1a-1d sweep is `ladder`. Your old habit of "claims = do stage-1 work" would silently skip 1a/1b.
      >
      >     🧑 "/haipipe-application claims"
      >             │
      >             ▼
      >        🔍 is the ladder virgin? (no 1a/1b docs)
      >        ├── no  ──▶ 🧾 rung 1c directly              (precision)
      >        └── yes ──▶ 💬 "1a/1b are empty — run `ladder`
      >                         for the sweep, or 1c anyway?"  (habit-safe)
      >
      >     A    always → 1c silently (as shipped; habit silently skips 1a/1b)
      >     B ✅ soft redirect on a virgin ladder (matches the router's existing offer-the-frontier pattern; one sentence in Dispatch notes)
      >     C    make `claims` alias the full sweep (loses precise 1c addressing)
      >
      > CC: my rec = B. Reply `> USER:` below.
      > JL: I agree.
      > CC: ✅ done — soft-redirect rule added to the Dispatch notes below.
      **@ haipipe-application/SKILL.md — venue for DESIGN-type interventions (ROUTED: Round-2 candidate in SOP-ladder-restage.md §10 — venue-design-doc pack, possibly a 2-design stage)**
      > JL: /haipipe-application venue "timing-aware refill nudge for patients" --no-pin <--- I think we need to think about what is the good venue here. My understanding is the Design artifacts requirements. Like the report. Like the final report of the generated messages.
      > CC: agreed — for DESIGN-type interventions the deliverable is really TWO artifacts: the message set itself + the design report that justifies it (A←C traces). Current packs cover the report half (venue-report) but not the message-set-with-rationale form. Captured as Round-2 candidate in SOP-ladder-restage.md §10 (a venue-design-doc pack, possibly paired with a 2-design stage — see the README Skill Structure thread); the bench run on 01_sms_young_male will show what the current packs lack.
      **@ the Stage Gate Protocol — ladder gate-batching depths (PARKED: bench run on 01_sms_young_male is the test; revisit at bench close-out, tracked in SOP-ladder-restage.md §10)**
      > CC: 🚪 the batching depths are CC defaults from SOP R6 — confirm.
      >
      >     🪜 ladder:      1a ──▶ 1b ──▶ 1c ──▶ 1d
      >     light  📱 :      ·      ·      ·     🚪  (one gate, 4 ledger rows)
      >     medium 📧 :      ·      ·     🚪     🚪
      >     full   📊 :     🚪     🚪     🚪     🚪
      >                                   ▲
      >                     💸 1c is where money is spent (full-mode probes)
      >
      >     A ✅ keep: medium gates at 1c — a human eyeballs the campaign where cost concentrates, 1b is cheap so it folds into the 1c gate
      >     B    medium at 1b+1d: earlier check on theme DIRECTION, but low value for the extra pause
      >     C    one gate at 1d for every venue: simplest, but deep venues lose rung-level control
      >
      > CC: my rec = A. Reply `> USER:` below.
      > JL: I am not sure here, but we can test it during the real use case.
      > CC: ✅ parked — depths stay as shipped; the 01_sms_young_male bench run is the test. Revisit this thread after it.
      **@ the README Skill Structure section — cumulative DIKW reading + 1d rename principles -> ADVICE (both executed)**
      > JL: I am thinking about how to distinguish D I K W with description theme claims and principles. So it is like description align to D, theme align to D + I, claims align to D + I + K, and principles aligns to D + I + K + W. I am not sure whether we want to have the name of principles, maybe insights or maybe what else? I think there are some design directions or insights which can help us to use in the later stage of Tools/plugins/haipipe-toolkit/skills/application/1-lifecycle/5-section-edit
      > CC: your CUMULATIVE alignment is better than my rung=letter framing — each rung CONTAINS its lower layers (a claim carries its D grounding + I pattern + K generalization; a principle carries all four). Adopting this as the canonical reading (SOP §10). On the 1d name: NOT "insights" — it collides head-on with the insight KB layer (/haipipe-insight, insights/ folders), the exact vocabulary clash we avoided by not reusing the D/I/K/W letters. Your own phrase "design directions" is the strong candidate: `1d-directions` (the 1d pun is free), it kills the standing double-use of "principles" vs venue Artifact Principles, and "directions" reads naturally as the thing section-edit/artifact CONSUME. Cost: ~20-mention sweep, cheap while nothing is filled. My rec: rename to 1d-directions before the bench run, or explicitly re-bless "principles". Reply `> USER:` with your pick.
      > JL (chat, 2026-07-09): rename to ADVICE — "later we can use them or not use them".
      > CC: ✅ executed — `1d-advice` / `haipipe-application-advice` / `A<n>` ids / maturity `advised`, plus the ADOPTION contract your ruling implies (advice = counsel, not mandate: downstream venue-ALIGNED stages record adopted/declined A-ids with a why; declined entries persist for the next venue/round; claim-audit chain = artifact -> adopted A -> C -> anchor). "principles" survives only as a legacy verb alias.
      **@ the README Skill Structure section — pitch/narrative/display fit for design tasks + a 2-design stage (ROUTED: Round-2 candidate in SOP-ladder-restage.md §10; bench run supplies the spec)**
      > JL: for now, I am not sure whether 2-pitch 3-narrarive 4-display is useful for the application design tasks. We can ignore it for now.
      > JL: but we still need pitch like to fit with the venue. and then we have the design. Maybe we need to have a design lifecycle stage. How do you think?
      > CC: agreed on both halves. Ignoring is already cheap: narrative/display are venue-GATED, so a design-type venue pack can set stages_skipped and they never fire — no surgery needed to "ignore for now". On the design stage: yes, I think it's real. Sketch (Round-2 candidate, SOP §10): for design venues (message set + design report), the venue-ALIGNED middle becomes  pitch(light: venue-fit only) -> 2-design -> draft. The 2-design stage owns the DESIGN MATRIX — segments x arms x framings, every cell citing the A<n> it applies and tagged exploit|explore (ties into the 1d strategy thread: explore arms are deliberate bets that the deployed A/B settles). Rather than build it blind, run the 01_sms_young_male bench with the current spine first; where pitch/draft strain to hold the matrix is exactly the spec for 2-design.
260709 · `6.1.1`
      - REVIEW SWEEP (fresh-eyes subagent audit after 6.1.0; all findings fixed same day). BLOCKER: the P->A id sweep had corrupted the literal `PP01` to `PA01` in 10 spots (claims SKILL + template, router example, fn/probe-plans, the Dashboard Contract) — card ids the check-probe-cards.sh `PP*.md` glob can never see; restored to PP01.
      - Trace contract completed onto the adoption chain (finishes R7/R9): artifact frontmatter `cited_K/cited_W` -> `adopted_A`/`declined_A`, slot examples cite A ids, review/check/claim-audit criteria now trace artifact -> adopted A -> C -> anchor; no insight-card citation is mandatory anywhere.
      - check-probe-cards.sh gains the two-level glob `0-lifecycle/*/*/_PROBE/PP*.md` (section-edit cards were invisible to VERIFY and the gate; the paper twin has the same blind spot — alignment-watch port candidate).
      - Residue sweep: 5 stray P ids -> A (the Intervention Lifecycle Contract, the Dashboard Contract, enter, claim-audit, iterate — iterate also fixes chain order to T/C/A); venue placement wording "after the ladder (1d gate), before pitch" (venue SKILL, the Intervention Lifecycle Contract, the README Skill Structure section); enter console gains ladder/descriptions/themes/advice verb rows; 13-key strip examples regenerated (enter, the Dashboard Contract); narrative-template "1d principles" -> advice; PHILOSOPHY "design principles" -> "design advice" (2x); "directives" -> "advice entries" (venue SKILL, pitch template); id examples unpadded C1/A1 (narrative, display, the Dashboard Contract); example task refs T<nn> -> X<nn>_<slug> (display, probe — T is the theme namespace); 1d-advice column re-padded in 7 ladder blocks; round triage gains advice + descriptions rung rows; README retired-spine row now shows the ladder; CHANGELOG titles fixed (advice/artifact/check); lifecycle CHANGELOG gains its missing 4.0.0 entry; versions bumped: router 6.1.1, narrative 4.2.0, display 4.2.0.
      - NOT fixed (user decision pending): `_archive/{haipipe-application-ask,haipipe-application-minimap}` is deleted in the working tree by an external change while the README Skill Structure section + fn/feedback.md still point at it — restore or update the docs.
      Archived comment threads — open at time of parking (2026-07-09, verbatim)
      --------------------------------------------------------------------------
      Parked at user request before the bench run; NO ruling yet on either. Both decisions remain live: the explore|exploit role tag is a Round-2 candidate (SOP-ladder-restage.md §10, pairs with the 2-design stage idea); the maturity vocab stands as written (`data-described` / `advised`) until renamed. Reply by reopening a `> USER:` thread in the source file or ruling at bench close-out.
      **@ 1-lifecycle/1d-advice/haipipe-application-advice/SKILL.md — derivation bars (CC defaults, unconfirmed) + explore|exploit role-tag proposal (OPEN)**
      > CC: ⚖️ these derivation bars are CC defaults (no ruling) — confirm the three levels.
      >
      >     🎯 A may cite...       light 📱   medium 📧      full 📊
      >     +--------------------+---------+--------------+--------+
      >     | ✅ supported claims |   ✔️     |     ✔️        |   ✔️   |
      >     | 🟡 weak + caveat    |   ✔️     | load-bearing⚠️|   ❌   |
      >     | 🔴 GAP-derived      |   ❌     |     ❌        |   ❌   |
      >     +--------------------+---------+--------------+--------+
      >       └─ the anti-fabrication floor: advice resting on NO evidence
      >          is a 🌱 seed hunch, not advice
      >
      >     A ✅ keep as written (GAP floor is the ladder's whole point)
      >     B    allow GAP-derived at light with a 🚩 flag (faster SMS drafting; re-opens the vibes hole)
      >     C    tighten medium to supported-only (slows email work for little gain)
      >
      > CC: my rec = A. Reply `> USER:` below.
      > JL: so the gap means this is not supported? right? and if so, sometime the message design can be really aggressive, like exploit something that is not supported? or something that is weak or not sufficient evidence? How do you think? That is the difference strategies.
      > CC: yes, GAP = no judged evidence yet. And your point is right — deliberately betting on unproven directions is a legitimate STRATEGY (test-to-learn), not a violation. Proposal: give every A a role tag `exploit | explore`. The bars above apply to EXPLOIT entries only; an EXPLORE entry may derive from weak/GAP claims PROVIDED it (a) carries the explore tag visibly, (b) states which C<n> the deployed arm will settle, and (c) stays inside compliance rails. The A/B result then flows back: iterate → 1a backfill → C flips → the explore entry either graduates to exploit or moves to Rejected. That makes deploy itself an evidence probe. Reply `> USER:` if you want this designed in (pairs with the 2-design stage idea -- Round-2 candidate in SOP-ladder-restage.md §10; that thread is archived in haipipe-application/CHANGELOG.md).
      **@ the README Skill Structure section — maturity vocab `data-described`/`advised` (CC-invented, unconfirmed; JL follow-up answered, no ruling) (OPEN)**
      > CC: 📶 maturity values `data-described` and `advised` are CC-invented names for the new ladder rungs (also in the Intervention Lifecycle Contract + the enter console) — confirm or rename.
      >
      >     📶 prospect → data-described → claim-ledger → advised → venue-pinned → ...
      >                   ▲ CC-invented ▲                ▲ CC-invented ▲
      >
      >     A ✅ keep both (finer console diagnosis; application already diverges from paper intentionally)
      >     B    mechanical names (1a-done / 1d-done): self-explanatory but ugly
      >     C    drop both, keep only claim-ledger (leanest — the strip already shows rung progress; defensible if you feel vocabulary creep)
      >
      > CC: my rec = A, with C as the lean alternative. Reply `> USER:` below.
      > JL: why it is here? I think we might have data, theme as well. what is the gap between the theme. I don't know. For the theme, it is supported by the description topics. but it can cover the content related to the descriptions in its own part.
      > CC: it's here because this file defines the maturity vocab. On "data, theme as well": maturity is deliberately COARSER than the strip — the strip already shows every rung, so maturity only marks capability jumps (data-described = grounded exploration possible; advised = artifact work possible). A `themed` value is easy to add if you want per-rung maturity; my lean is no. On the theme/description gap: your cumulative-DIKW reading answers it (adopted as canon; that thread is archived in `../haipipe-application/CHANGELOG.md`) — a theme may carry its OWN theme-scoped descriptive content (its D-layer) inside its part, as long as numbers stay anchored (pointer + date); a number that becomes load-bearing across rungs gets promoted to a 1a D entry.
260709 · `6.1.2`
      - BENCH FINDING (first live run, 01_sms_young_male): Probes roster section made uniform across all four ladder rungs. Only seed + 1c-claims stage docs listed their probes; 1a/1b/1d had none, so the user could not see a rung's probe sessions in the stage doc (JL: "we should also have the probe sessions like we have in 0-seed.md"). Templates + SKILL content-structure + done-criteria updated (descriptions 1.1.0, themes 1.1.0, advice 1.2.0); roster must match _PROBE/ on disk; in 1a the section sits between Descriptions and Refresh Log, with D-slots referencing entries via [AWAITING PP<nn>].
      - Live-intervention bookkeeping (01_sms_young_male): 0-seed.md PP01 roster line refreshed dispatched -> read with the landed answer (novelty gap confirmed, backs C5). The 1a Probes section + the 1c-claims folder migration + index re-point were done by the operator's parallel session; the 1a template ordering follows that live doc.
      - Still open from the bench (Round-2 spec, not yet implemented): migrate step for legacy paper-style interventions (enter offers it on drift), eager scaffold of the venue-FREE spine at get-or-create, probe-release-requires-approval encoded in the probe worker, PHI column-scope defaults to restricted allow-list without asking.
260709 · `6.2.0`
      - BREADTH ROUND (JL flywheel discussion, same day as the bench run): the ladder is codified as an insight-discovery FLYWHEEL — three nested loops (inner: multi-round DPRC within a rung, loop-until-dry; middle: routing rounds across rungs, mid-phase [ROUTE -> <rung>] legal; outer: deploy/iterate -> new data -> 1a refresh). README gains "The ladder is a flywheel" section (diagrams + lens/reservoir table); the Stage Gate Protocol gains the Rounds contract (venue-scaled round depth: light one round, medium loop-until-dry on 1c, full everywhere); lifecycle sweep re-enters routed-to rungs (4.1.0).
      - Per-rung breadth contracts: 1a Coverage six facets filled-or-waived (1.2.0); 1b three lenses incl. counter-hunt + full D-consumption (1.2.0); 1c full hook consumption (Declined-hooks section) + Rival line + refute-capable probes (6.1.0); 1d full C-consumption + No-action line + negative advice (1.3.0). Every rung names its reservoir (waived facets / Parked / Declined hooks / Rejected), re-mined at each DRAFT open.
      - EXPLORE|EXPLOIT ADOPTED at 1d (resolves the parked derivation-bars thread in the open-thread archive above): settlement bars scope to exploit entries; explore = tagged test-to-learn bet naming its settling C + rails; graduates via iterate; adopted explore entries keep the tag in artifact frontmatter (artifact SKILL updated). Deploy itself becomes an evidence probe.
260709 · `6.3.0`
      - ROUND-2 CLOSE-OUT (the four still-open bench findings from 6.1.1/6.2.0, all encoded): enter 2.1.0 — eager venue-FREE spine scaffold at get-or-create + confirm-gated one-shot legacy migration (1-claims -> 1c-claims, rung scaffold, probe re-file by shape); probe worker 2.1.0 — STEP 1.5 RELEASE GATE (user releases planned cards; roster + stop otherwise) + PHI restricted-columns-by-default on task dispatches; PREFERENCES.md gains the release rule as a portable global pref; README retired-names row points at the enter migration.
      - Session-role note (JL): skill-dev sessions update the skills; running interventions belongs to operator/test sessions. The 01_sms_young_male state advanced earlier this session (seed REVISE, 1a coverage round) stands as the worked example; its two pending gates (seed approval, PP02 release) belong to the test session.
      - Follow-up (JL, same day): "at the end of each draft, it should let me know what probes to release as well" -> draft worker 1.3.0 gains step 5 PRESENT (every DRAFT ends with the RELEASE MENU -- buffered planned cards, one line each -- and stops for picks; return contract gains `probes:`); probe worker STEP 1.5 stays as the backstop for DRAFT-skipping paths; PREFERENCES entry updated.
      - Follow-up (JL, same day): default reply mode for all family skills = /diagram-ascii (PREFERENCES entry strengthened from "communicate via ASCII diagrams" to THE default mode: emoji-rich diagrams carry the substance, prose reduced to one-line asks).
260709 · `6.4.0`
      - GROW LOOP at 1a (JL: "iterate to build and grow up until you have more and more probes to better understand the data to describe the data, and then go to the next stage" + "after the check, they can think about adding more probes in the draft"): descriptions 1.3.0 — rounds run as a saturation engine (question storms with rotating lenses per new ref/interrogation-battery.md, answerable-filter, blind self-test, venue-scaled dry-stop; landed numbers feed the next round, so the probe roster grows lap by lap); Field Disposition (100% of schema: profiled | waived | excluded, column names only) with new `_DESCRIPTIONS/DS<n>` per-dataset profile sheets as the home; probe worker 2.2.0 redirects the values lane there for rung 1a; check worker 4.1.0 gains the `grow` verdict (the gate asks for missing topics — the USER lens; grow re-opens DRAFT as [ROUND n+1]; approve = saturated AND user added nothing); the Stage Gate Protocol + README updated.
      - Follow-up (JL, same day: "some probes can just be the task folder, no need to have a new task group folder"): granularity ladder encoded at three points -- task-orchestrator agent 1.1.0 gains the LAND rung (config variant > new task in group > new group last-resort, one need = one task/config), probe worker 2.3.0 dispatch prompt carries task_landing, battery rails note GROW grows probes not folders. Trigger: SMSDesign tasks/ grew 7 full scaffolds for 7 profile queries on one parquet.
      - Feedback-inbox loop goes live (bench-invented convention, adopted): skills carry a `feedback/` inbox (`<YYYY-MM-DD>_<slug>.md`, `status: open|fixed`, filed via `/haipipe-application feedback` at capture-time routing); the skill-dev session processes items and records `fixed_in`. First item processed: enter 2.2.0 Releasable Probes dashboard block.
      - Follow-up (JL, same day: "different config and different run.sh can mean different subgroups... tasks should be flexible with config.yaml and run.sh"): the ladder's rung (a) gets its mechanism, grounded in /haipipe-task ref/task-structure.md (one config = one run.sh, results name-paired). Task-orchestrator agent 1.2.0: LAND naming rule -- task folders segment/dataset-agnostic (`01_arm_engagement`, never `01_young_male_arm_engagement`); segment filters + input dataset paths are config keys; hardcoded slices get externalized in a BUILD touch-up, not cloned. Probe worker 2.4.0: task_landing dispatch line carries the same rule. Battery rail: a new cohort re-runs the whole battery by adding configs, never by re-scaffolding.
260717 · `6.5.0`
      - Match paper's "no proxy verb" style (paper 3.1.0, 2026-07-14 — application predated it by 5 days): DROP the `discover` and `task` verbs from the umbrella. Reaching the bank is the PROBE phase's job, not the intervention's; a human doing standalone utility (a lit scan, a data check) types the bank's OWN door `/haipipe-task qa` | `/haipipe-discovery qa`, never proxied by the intervention.
      - Removed: the two verb rows, their Dispatch-notes rows, the discover Example line, the "Direct task/discover verbs remain…" description clause, `discover|task` from the No-Arg Chooser.
      - Added / rerouted to mirror paper verbatim: the intro no-proxy principle paragraph; Delivery Need Routing "standalone utility (a HUMAN…) -> /haipipe-task qa | /haipipe-discovery qa (the bank's own door)"; the Composing tail "a stage reaches the bank ONLY through its PROBE phase — no direct discover/task verb".
      - Scope: discover/task only; insights cleanup and the "stages × four phases" teaching block deliberately NOT bundled in.
260717 · `6.6.0`
      - Family insight-KB sweep: the insight KB is retired as an evidence layer (evidence lives in the probe -> task/discovery bank; the deliverable W lives in `1d-advice.md`). This file drops `and insights` from the intro and removes the `/haipipe-insight` delivery-need route. Paired removals across enter/claim-audit/artifact/section-edit/1a/1d/iterate + the wiki index/PHILOSOPHY; the retired `ref/application-input-contract.md` deleted.
260717 · `6.7.0`
      - Align dir naming to paper + fold audience into venue. `_venue/` -> `venue/` (no underscore, matching `paper/venue/`) across every live reference (~12 files). `_audience/` DELETED: the separate audience-profile packs are gone; the venue pack's style-profile carries tone-by-audience (the audience axis), per JL ("audience should be with venue"). Dead `_audience/` path pointers removed/redirected in umbrella/lifecycle/draft/revise/narrative/artifact/review + venue/_SCHEMA + venue-sms + README/wiki. Audience remains a targeting + tone axis; only the standalone directory is retired.
260717 · `6.8.0`
      - Delivery layer renamed `3-build-deploy` -> `3-deliver` to match `paper/3-deliver` (paper reshaped its build/submit layer into a 4-substage pipeline; application adopts the NAME + verb-intent but stays FLAT — markdown/channel artifacts have no LaTeX build/polish/ship sub-stages to fill, per option B). Added `3-deliver/README.md` (intent gradient: compose -> audit -> ship). All live path references updated; SOP history left as-is.
260719 · `6.8.1`
      - `fn/probes.md` synced to probe constitution v9.5.0 (the Q-executor-entry format). The anatomy example is now a `## QX<n>` ENTRY with four `###` subsections — `### q-executor` (+ Deliverable/Accepted), `### q-consumer` (one bullet per served Q-consumer: its stage-doc id + original question), `### bank binding` (`**route**` / `**bank**`: reuse|run|code|new / `**target**` / `**state**`), `### a-executor` (the copied QA answer). Renames: `serves:`→`### q-consumer`, `match:`→`bank`, the probe-file `a-consumer:`→`### a-executor`; `## Why` DROPPED (the stake lives in each stage-doc Q-consumer). States table updated (`read` = `### a-executor` non-empty); BUILD-lane fields moved under `### bank binding`. Loop section now shows the settled phase split: DRAFT authors ①ORGANIZE+②MATCH, PROBE runs ③④⑤ and does not re-match. `_VALUES_`/`_CITATION_` sidecars retired — `1-probes/` is the only consumer-side source of truth, `_LOG` the only kept sidecar. This file carries no `metadata.version` of its own, so the sync is recorded here against the umbrella.
260719 · `6.8.2`
      - WIKI RETIRED. The `application/wiki` bucket is dissolved: each doc moved into its ONE natural owner skill, and every inbound reference now points at that owner. No doc content is duplicated across skills — referrers point, they do not copy.
      - This file's SKILL.md becomes the family's shared-convention home and gains TWO sections: **Stage Gate Protocol** (from `08-stage-gate.md`, the most-referenced doc at 15 referrers) — gate loop, venue-scaled depth, ladder gate batching, the ladder routing invariant, the Rounds-within-a-rung breadth/depth contract, mechanical teeth, Gate Ledger schema, autonomy policy, recovery; and **Delivery Need Routing** (from `11-delivery-need.md`, merged into the existing routing section rather than added beside it) — how the application talks to the bank, when to raise a question, routes, the `## QX<n>` question record, and the backfill direction.
      - Other homes: `03-intervention-lifecycle.md` -> `1-lifecycle/haipipe-application-lifecycle/SKILL.md` (Intervention Lifecycle Contract); `06-application-skill-structure.md` -> `README.md` (Skill-tree layout + Stage to Procedure + Router Rule + Maturity Rule); `05-intervention-dashboard.md` -> `0-enter/haipipe-application-enter/SKILL.md` (Dashboard Contract); the wiki index README dropped (a pure index, nothing to rehome).
      - Rewired ~45 inbound references across SKILL.md files, `README.md`, `EVALUATION.md`, `2-phase/USAGE.md` + `WIRING.md`, `SOP-ladder-restage.md`, `SOP-paper-alignment.md`, `stage-strip.sh`, `ref/interrogation-battery.md`, and the family CHANGELOGs — relative depth recomputed per referring file. Archived history now names the CONTRACT ("the Stage Gate Protocol") instead of a retired path.
      - Also dropped: the `_archive/` row in the skill-tree (the directory no longer exists on disk) and the paper-side evidence-principles path in References (the four evidence principles stay SHARED paper-owned doctrine, now named without a path since the paper wiki is being retired in parallel).
      - Prose archaeology stripped from every line touched: `(JL ruling <date>)`, `(JL <date>)`, and ruling-id citations in live prose. Archived `> CC:` / `> JL:` threads left verbatim.

<!-- haipipe:skill:log:end -->
