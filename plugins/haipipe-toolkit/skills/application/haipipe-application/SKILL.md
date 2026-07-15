---
name: haipipe-application
description: "Run any intervention-lifecycle work (the application umbrella). Use `/haipipe-application enter <intervention-path>` or `status` to preload an open-needs dashboard from STATUS.md, 0-lifecycle, 0-artifacts, 1-rounds, and git state. Application lifecycle owns intervention-specific story, claims, narrative, displays, artifact text, maturity, and dated work rounds; the venue (sms/email/dashboard/report/...) gates which stages fire and how deep claims must settle; open questions accumulate as SECTIONS in probe files under 1-probes/PPNN_<topic>.md, consumed by haipipe-application-probe (each stage's PROBE phase worker), which binds each question to a QA file in the task/discovery bank by dispatching the commission through a clean agent -- the intervention never calls the bank directly. Trigger: application, intervention, enter, status, seed, claims, venue, pitch, narrative, display, section-edit, draft, sms, message, email, dashboard, report, review, deploy, iterate, round, probe, /haipipe-application."
argument-hint: "[enter|status|venue|stage|draft] [intervention-path-or-args...]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "5.3.0"
  last_updated: "2026-07-14"
  summary: "Front door for the intervention lifecycle (paper-aligned): parse intent (venue + stage), route to the stage specialists. Each stage runs four phases (draft → probe → revise → check); the intervention RAISES evidence questions as sections in 1-probes/, and each stage's PROBE phase dispatches them through a clean agent — the intervention never calls the bank directly. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application (orchestrator)
==========================================

User-facing entry for the intervention lifecycle. The application lifecycle is a delivery owner: it owns this intervention's story, claims, narrative, displays, artifact text, maturity, and dated work rounds. Project-level evidence lives outside the intervention in discoveries and tasks; when a stage hits a gap, record a delivery need (`../wiki/11-delivery-need.md`) and route to the evidence worker.

This orchestrator parses intent and dispatches to stage/specialist skills via `Skill()`. Stage skills internally drive the DPRC phase workers (`2-phase/`); users and this router never invoke phase skills directly. PROBE ends with a VERIFY step (the probe worker's deterministic card checker), and CHECK runs `checks.sh` plus re-runs the card checker as the gate's teeth. Canonical structure: `README.md` at the application skill root + `../wiki/06-application-skill-structure.md`.

ALWAYS read and honor `PREFERENCES.md` (this skill's own folder): portable, git-tracked global behavioral preferences that survive a machine change. `digest` / `feedback` append flagged global prefs there (merge-or-create).

Verbs
------

One block: verb, aliases and trigger keywords, then where it goes.

```
enter | status | dashboard | preload         -> haipipe-application-enter (open-needs console; GET-OR-CREATE: a missing path offers to scaffold the intervention first; also "enter intervention", "new intervention")
venue | format | modality | channel          -> haipipe-application-venue (recommend + pin; sms/push/reminder/checklist/email/dashboard/ui-card/report all land here; pin writes venue + stages_skipped + claims_settlement into STATUS.md AND produces 0-lifecycle/2-venue/2-venue.md with Artifact Principles — the downstream contract pitch/display/section-edit read)
seed                                         -> haipipe-application-lifecycle seed        (also "opportunity", "why might this work", "kill criteria")
claims | claim | ledger                      -> haipipe-application-lifecycle claims      (also "what must be true", "evidence plan", "claim gap", "supported", "GAP")
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
probe ["<question>"] | probe | probe run [PPNN] -> probe files: 1-probes/PPNN_<topic>.md, one SECTION per question (RAISE / SHOW the board / "run" hands them to haipipe-application-probe; also "evidence gap", "verify claim", "hypothesis")
feedback "<text>" | feedback list|move       -> fn/feedback.md (resolve BEFORE other parsing)
digest [session] [--dry-run]                 -> fn/digest.md   (resolve BEFORE other parsing)
"<natural language>"                         -> infer via the keywords above, dispatch
```

Examples:

```
/haipipe-application enter "examples/Project-SMSR/applications/interventions/03_refill_reminder"
/haipipe-application venue "timing-aware refill nudge for patients" --no-pin
/haipipe-application claims
/haipipe-application probe "C02: timing matters for refill response"
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

Venue coupling (drives two routing rules): seed + claims are venue-FREE; venue pins the modality in STATUS.md between claims and pitch (writing `| venue |`, `| stages_skipped |`, and `| claims_settlement |` rows) and writes `0-lifecycle/2-venue/2-venue.md` with Artifact Principles; pitch/narrative/display/section-edit are venue-ALIGNED and read those Artifact Principles (consulting `_venue/venue-<name>` only for detail beyond them). So: "application" with claims done but no venue pinned -> run `venue` before pitch. Re-targeting ("turn this into a dashboard") -> re-run `venue`; pitch re-couples; claims stays unchanged, only its REQUIRED SETTLEMENT deepens or relaxes.

Dispatch notes (only where non-obvious; everything else is `Skill("haipipe-application-<target>")` or `Skill("haipipe-application-lifecycle", args="<verb> ...")`):

```
enter     Path exists -> Skill("haipipe-application-enter", args="<path>"). Path MISSING -> get-or-create:
          CONFIRM FIRST (never create off a typo). Interventions are plain folders (no repo backing):
          scaffold STATUS.md + 0-lifecycle/ + 0-artifacts/ + 1-rounds/ + 1-probes/ under
          the project's applications/interventions/<NN>_<slug>/, then continue straight into the console.
probe     Three sub-modes -- "<question>" RAISE it as a SECTION in the right topic's probe file under
          1-probes/ (creating PPNN_<topic>.md if the topic is new), no args SHOW the board (DERIVED
          from 1-probes/ on disk, never a stored status),
          "run [PPNN]" -> Skill("haipipe-application-probe", args="from-buffer <intervention_root> [PPNN]").
          This umbrella NEVER dispatches evidence agents itself: the five-step loop runs inside a stage's
          PROBE phase via haipipe-application-probe, which MATCHes against the bank's QA corpus first and
          only then dispatches a commission onward. Readings backfill into 1-claims / sections / round
          logs -- and a claim's STATUS lands in 1-claims.md, never in a probe. Convention: fn/probes.md.
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
stage:   seed ✅  claims 🔥🚀  venue ⬜  pitch ⬜  narrative --  display --  section-edit --  →  draft ⬜  →  review ⬜  →  deploy ⬜
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

Markers: 🔥 active now (what this session works on) · 🚀 frontier (farthest the intervention has ever reached) · ✅ done (Gate-Ledger-approved; venue slot: pinned) · ⬜ not started · `--` skipped by the pinned venue. Rules: EXACTLY one 🔥 and EXACTLY one 🚀 per line, never zero -- "reached" means entered, not completed, so a virgin intervention working its first phase renders `draft 🔥🚀`; they split only on loopback (the frontier slot keeps 🚀 while 🔥 moves back) and collapse to `🔥🚀` when they land on the same slot; the phase line always describes the 🔥 stage's DPRC phases. Venue-skipped stages render `--` and can never carry 🔥 or 🚀.

Render the stage line DETERMINISTICALLY with the helper (never hand-type it; it drifts): `sh "$CLAUDE_SKILL_DIR/stage-strip.sh" <intervention-dir> [<session-stage>]` (the script lives IN this skill folder, next to this spec; it reads `| current_layer |`, `| venue |`, `| stages_skipped |`, and the Gate Ledger from STATUS.md). The phase line is rendered by the 🔥 stage's skill from its own DPRC progress.

Gate-aware: advancing `current_layer` requires an EXPLICIT approval action that the current stage is done (Stage Gate, `../wiki/08-stage-gate.md`) -- by the human (copilot mode) or by the check worker's persona standing in (autopilot/unattended modes); once STATUS.md carries the gate ledger, ✅ means "approved", and the ledger records who approved.

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

Application work is demand-driven: a claim, content element, artifact slot, or round todo may reveal that the next action is evidence work. The enter/status path surfaces those needs before recommending more drafting. Need record schema + boundary: `../wiki/11-delivery-need.md`.

```
claim needs evidence / robustness / literature / a data artifact -> /haipipe-application probe "<question>"  (a SECTION in 1-probes/; the PROBE phase matches the bank first, dispatches only what is missing)
display element needs materialized output (not claim-gated)      -> /haipipe-task-for-display <need>
a question with no intervention behind it                        -> /haipipe-task qa "<q>" | /haipipe-discovery qa "<q>"  (the QA file IS the receipt; no probe file needed)
the claim's STATUS once the evidence lands                       -> 0-lifecycle/1-claims/1-claims.md  (there is no probe "verdict" — the word is retired)
wording/structure/tone                                           -> the owning lifecycle stage skill (audience profile shapes tone)
```

ALL evidence enters through a stage's PROBE phase; the intervention never calls the bank directly. Resolved evidence backfills into `1-claims`, `4-display`, sections, or round logs. Executors never own the intervention story — and the intervention never writes in the executors' bank (LAW 1: a consumer session never executes task/discovery work inline).

Structure Pointers
-------------------

Each area's internal contract lives with its owner; consult, never restate:

```
skill tree (0-enter / 1-lifecycle / 2-phase / 3-build-deploy / 4-iterate / wiki)
                                   -> README.md (skill root) + ../wiki/06-application-skill-structure.md
intervention-folder layout         -> README.md (skill root) + ../wiki/03-intervention-lifecycle.md
lifecycle stages + venue gating    -> ../wiki/03-intervention-lifecycle.md
rounds                             -> 0-enter/haipipe-application-round (same vYYMMDD contract as paper)
venue knowledge                    -> ../_venue/venue-<name> packs (venue is knowledge, not a pipeline)
audience knowledge                 -> ../_audience/profile-<name> packs
```

Composing with Evidence Workers
--------------------------------

```
/haipipe-application (router)
        ├─► /haipipe-application-lifecycle   (seed -> claims -> [venue] -> pitch -> narrative° -> display° -> section-edit°)
        ├─► /haipipe-application-artifact    (draft the deliverable from the venue profile + lifecycle stages)
        │
        │   evidence path (a stage's DRAFT raises a question):
        └─► 1-probes/PPNN_<topic>.md  ─►  haipipe-application-probe (the PROBE phase worker)
              ①ORGANIZE ②MATCH ③DISPATCH ④POINT ⑤INTERPRET
                    │
                    │  ② MATCH the bank's QA corpus FIRST — most questions stop here (T2 REUSE)
                    │  ③ only what is left: the `commission` block, VERBATIM, to
                    ├─────► Agent(haipipe-task-orchestrator-agent)        ─┐  clean context
                    └─────► Agent(haipipe-discovery-orchestrator-agent)   ─┘  IS the wall
                              └─► the executor runs its own `qa` gate and writes
                                  <task-folder>/QA/<n>-<slug>.md   ← the answer, in GENERAL language
                                    └─► the section's target: points at that FILE; its reading:
                                        interprets it; the CLAIM's status flips in 1-claims.md

        a stage reaches the bank ONLY through its PROBE phase — no direct discover/task verb
```

Feedback & Digest
------------------

`/haipipe-application feedback "<text>"` captures a complaint/wish about THIS skill family, capture-time-routed into the concerned sub-skill's `feedback/` inbox (folder = the record; orchestrator inbox is the fallback), MERGE-OR-CREATE so inboxes stay self-limiting; `feedback list [skill]` aggregates, `feedback move <file> <skill>` re-routes. `/haipipe-application digest [session] [--dry-run]` harvests a session transcript into discrete feedback items (dedup, mandatory confirm gate, then the same capture; global behavioral prefs fan out to every orchestrator's PREFERENCES.md instead of the inboxes). Full spec: `fn/feedback.md` + `fn/digest.md`; this section is a pointer, not the spec.
