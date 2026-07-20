---
name: haipipe-application
description: "Run any intervention-lifecycle work (the application umbrella). Use `/haipipe-application enter <intervention-path>` or `status` to preload an open-needs dashboard from STATUS.md, 0-lifecycle, 0-artifacts, 1-rounds, and git state. Application lifecycle owns intervention-specific story, the stage-1 evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice), narrative, displays, artifact text, maturity, and dated work rounds; the venue (sms/email/dashboard/report/...) gates which stages fire and how deep claims must settle; open evidence questions are RAISED as entries in the flat probe pool 1-probes/PPNN_<topic>.md, and each stage's PROBE phase (haipipe-application-probe) binds them to answers in the task/discovery bank through a clean collector agent — never calling the bank directly. Trigger: application, intervention, enter, status, seed, ladder, descriptions, themes, claims, advice, venue, pitch, narrative, display, section-edit, draft, sms, message, email, dashboard, report, review, deploy, iterate, round, probe, /haipipe-application."
argument-hint: "[enter|status|venue|stage|draft] [intervention-path-or-args...]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "6.10.0"
  last_updated: "2026-07-19"
  summary: "Front door for the intervention lifecycle: parse intent (venue + stage), route to the stage specialists. Each stage runs four phases (draft → probe → revise → check); the intervention RAISES evidence questions as entries in the flat pool 1-probes/, and each stage's PROBE phase binds them to answers in the task/discovery bank through a clean agent — never calling the bank directly. The venue gates which stages fire and how deep claims settle; the 1a–1d ladder (D→I→K→W) is the venue-free evidence spine. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

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
probe ["<question>"] | probe | probe run [PPNN]  -> the flat probe pool 1-probes/PPNN_<topic>.md, one file per TOPIC, one `## QX<n>` ENTRY per q-executor (RAISE a question / SHOW the board / RUN the five-step loop; "run" hands the pool to haipipe-application-probe, the single door to the bank; also "evidence gap", "verify claim", "hypothesis")
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
probe     Operates on the flat cross-stage pool (1-probes/PPNN_<topic>.md; the README board is derived
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

A need is a QUESTION the intervention cannot answer itself. It is RAISED as a `Q-<Stage>-<n>` in the stage doc's Q-consumer section — which is where its STAKE lives — and bound to the bank by an ENTRY in the flat probe pool `1-probes/PPNN_<topic>.md`. No message bus, no shared contract file. Two channels carry it, and the agent (this session) is the medium:

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
2. Disk      the question lives as an ENTRY (`## QX<n>`) in 1-probes/PPNN_<topic>.md;
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

Each open question is one ENTRY in `1-probes/PPNN_<topic>.md` (anatomy + states: `fn/probes.md` and `../../probe/haipipe-probe/SKILL.md`). One file per TOPIC; one `## QX<n>` entry per Q-EXECUTOR, each with four `###` subsections — the file is Q-executor-oriented, and the consumers hang off it:

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
        └─► questions RAISED as entries in 1-probes/PPNN_<topic>.md  ─►  haipipe-application-probe (the PROBE phase worker)
                                            └─► Agent(haipipe-probe-q-executor-agent)  (stake-free collector; dispatches /haipipe-task + /haipipe-discovery)
                                                 └── answers land as QA files; the a-consumer + 1c-claims status backfill into the ladder, sections, round logs

        a stage reaches the bank ONLY through its PROBE phase — no direct discover/task verb
```

Feedback & Digest
------------------

`/haipipe-application feedback "<text>"` captures a complaint/wish about THIS skill family, capture-time-routed into the concerned sub-skill's `feedback/` inbox (folder = the record; orchestrator inbox is the fallback), MERGE-OR-CREATE so inboxes stay self-limiting; `feedback list [skill]` aggregates, `feedback move <file> <skill>` re-routes. `/haipipe-application digest [session] [--dry-run]` harvests a session transcript into discrete feedback items (dedup, mandatory confirm gate, then the same capture; global behavioral prefs fan out to every orchestrator's PREFERENCES.md instead of the inboxes). Full spec: `fn/feedback.md` + `fn/digest.md`; this section is a pointer, not the spec.
