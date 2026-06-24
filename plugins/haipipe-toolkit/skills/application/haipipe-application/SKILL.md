---
name: haipipe-application
description: "Application layer orchestrator (the application umbrella). Routes every session-style workflow in the haipipe stack: intervention lifecycle (seed → pitch → [venue] → claims → narrative → display → minimap → draft → review → deploy → iterate) and research questions (ask). Same stage vocabulary as paper. Venue (SMS, checklist, dashboard, report, etc.) determines which stages fire, claims depth (light/medium/full), and whether gates run. One generic draft skill reads the venue profile — no format-specific sub-skills. Trigger: ask, question, session, intervention, enter, status, seed, pitch, venue, claims, narrative, display, minimap, draft, review, deploy, iterate, round, sms, message, /haipipe-application."
argument-hint: "[verb] [intent...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "4.0.0"
  last_updated: "2026-06-23"
  summary: "Application layer orchestrator — venue-driven lifecycle, single draft skill."
  changelog:
    - "4.0.0 (2026-06-23): remove format specialists (message/ui/report) — absorbed into venue profiles; remove context + plan skills — absorbed into lifecycle orchestrator and claims stage; single draft skill reads venue profile."
    - "3.0.0 (2026-06-23): rename stages to paper vocabulary; add venue; venue-driven stage requirements."
    - "2.0.0 (2026-06-22): restructured around intervention lifecycle."
    - "1.0.0 (2026-05-31): baseline."
---

Skill: haipipe-application (orchestrator)
==========================================

User-facing entry for every **session-style workflow** in the toolkit.
An intervention = one user intent, one lifecycle folder, one set of
evidence-backed artifacts.


Core idea
==========

Same lifecycle vocabulary as paper. The **venue** (output modality)
determines which stages fire, how deep claims goes, and whether
gates run.

```
Simple (SMS):      seed → pitch → claims(light) → draft
Medium (email):    seed → pitch → claims(medium) → narrative → draft
Complex (dashboard): seed → pitch → claims(full) → narrative → display → minimap → draft
```

One draft skill reads the venue profile — the venue profile IS the
instruction set. No format-specific sub-skills.


Architecture (v4)
===================

```
application/
├── haipipe-application/              ← THIS: router + umbrella
│
├── 0-enter/                          Intervention Console
│   └── haipipe-application-enter/      derive-from-disk dashboard
│
├── 1-lifecycle/                      Per-stage skills (same names as paper)
│   ├── haipipe-application-lifecycle/  stage orchestrator (venue-aware)
│   ├── haipipe-application-seed/       Stage 0: opportunity
│   ├── haipipe-application-pitch/      Stage 1: one-sentence goal
│   ├── haipipe-application-venue/      Venue selection (pins in STATUS.md)
│   ├── haipipe-application-claims/     Stage 2: K/W selection or claim ledger
│   ├── haipipe-application-narrative/  Stage 3: arc structure (venue-gated)
│   ├── haipipe-application-display/    Stage 4: content elements (venue-gated)
│   └── haipipe-application-minimap/    Stage 5: widget jobs (venue-gated)
│
├── 2-rounds/                         Feedback + iteration cycles
│   └── haipipe-application-round/
│
├── 3-draft/                          Single draft skill
│   └── haipipe-application-draft/      reads venue profile, generates artifact
│
├── 4-review-deploy/                  Review + ship
│   ├── haipipe-application-review/     artifact review
│   ├── haipipe-application-claim-audit/ claim-evidence audit
│   └── haipipe-application-deploy/     deploy to channel (stub)
│
├── 5-iterate/                        Post-deploy refinement
│   └── haipipe-application-iterate/
│
├── _venue/                           Venue profiles (knowledge, not skills)
│   ├── venue-sms/                      README + style-profile + exemplars/
│   ├── venue-push/
│   ├── venue-reminder/
│   ├── venue-checklist/
│   ├── venue-email/
│   ├── venue-dashboard/
│   ├── venue-ui-card/
│   ├── venue-report/
│   └── _SCHEMA.md
│
├── _audience/                        Audience profiles (knowledge)
│   ├── profile-patient/
│   ├── profile-clinician/
│   ├── profile-regulator/
│   ├── profile-executive/
│   └── _SCHEMA.md
│
└── shared/                           Cross-cutting machinery
    ├── haipipe-application-ask/        evidence engine (full-claims GAPs)
    └── haipipe-application-gate/       phase gate (venue-gated)
```


Stage requirements per venue
==============================

```
                    seed   pitch   claims   narrative   display   minimap   gate
                    ─────  ─────   ──────   ─────────   ───────   ───────   ────
venue-sms           req    req     req      skip        skip      skip      skip
venue-push          req    req     req      skip        skip      skip      skip
venue-reminder      req    req     req      skip        skip      skip      skip
venue-checklist     req    req     req      optional    skip      skip      optional
venue-email         req    req     req      req         optional  skip      optional
venue-dashboard     req    req     req      req         req       req       req
venue-ui-card       req    req     req      req         req       optional  req
venue-report        req    req     req      req         req       req       req
```


Claims depth per venue
========================

```
light    (sms, push, reminder)         select K/W for template slots
medium   (checklist, email)            select + gap check
full     (dashboard, ui-card, report)  claim ledger + probe plans
```


Two shaping axes
=================

**Venue** = structure, constraints, which stages fire, claims depth.
**Audience** = tone, language, citation format, evidence depth.

Both are knowledge (profiles), not skills. Venue is primary
(structure). Audience is secondary (style within structure).


Commands
=========

```
/haipipe-application enter <path>          Intervention Console
/haipipe-application status [path]         dashboard
/haipipe-application seed                  Stage 0
/haipipe-application pitch                 Stage 1
/haipipe-application venue [name]          pin venue
/haipipe-application claims                Stage 2 (depth per venue)
/haipipe-application narrative             Stage 3 (if venue requires)
/haipipe-application display               Stage 4 (if venue requires)
/haipipe-application minimap               Stage 5 (if venue requires)
/haipipe-application draft                 generate artifact (reads venue profile)
/haipipe-application review                review artifact
/haipipe-application claim-audit           claim-evidence audit
/haipipe-application deploy                deploy (stub)
/haipipe-application round [new|triage]    round management
/haipipe-application iterate               post-deploy refinement
/haipipe-application probe run             batch-dispatch probe plans
/haipipe-application ask <question>        evidence session (legacy/direct)
/haipipe-application feedback "<text>"     capture skill feedback, ROUTED to the sub-skill it concerns
/haipipe-application feedback list [skill] aggregate open items across ALL inboxes
/haipipe-application feedback move <file> <skill>   re-route a mis-filed item
/haipipe-application digest ["<session-name|id>"] [--dry-run]  harvest a session (named/id'd PAST session, or current): distill + dedup + route feedback (confirm-gated)
```


Verb Map
=========

```
verb                                          → dispatch
────────────────────────────────────────────────────────────
enter, status, dashboard                      → haipipe-application-enter
seed, opportunity, why                        → haipipe-application-seed
pitch, goal, story                            → haipipe-application-pitch
venue, format, modality, sms, dashboard, ...  → haipipe-application-venue
claims, K/W, evidence, what must be true      → haipipe-application-claims
narrative, arc, structure                     → haipipe-application-narrative
display, panels, widgets, elements            → haipipe-application-display
minimap, jobs, assignments                    → haipipe-application-minimap
draft, write, create, generate, make          → haipipe-application-draft
review, check, compliance                     → haipipe-application-review
claim-audit, verify claims                    → haipipe-application-claim-audit
deploy, ship, go live                         → haipipe-application-deploy
round, iteration                              → haipipe-application-round
feedback "<text>"                             → fn/feedback.md handler (capture, route at capture, merge-or-create)
feedback list [skill]                         → fn/feedback.md handler (aggregate open items)
feedback move <file> <skill>                  → fn/feedback.md handler (re-route mis-filed item)
digest ["<session-name|id>"] [--dry-run]      → fn/digest.md handler (harvest a named/id'd PAST or current session, route via feedback)
iterate, A/B, performance                     → haipipe-application-iterate
probe, probe run                              → shared/haipipe-application-ask
ask, question, research                       → shared/haipipe-application-ask
message, msg                                  → haipipe-application-draft (venue=sms)
(no verb, intervention path given)            → haipipe-application-enter
```

Route a `feedback` first-token to the feedback handler BEFORE other parsing
(capture is MERGE-OR-CREATE: a same-topic complaint updates the existing inbox
file instead of spawning a duplicate). Likewise route a `digest` first-positional
to the digest handler (target=digest) BEFORE other parsing; resolve the target
session first (no arg = current, id = that .jsonl, name = grep the rename).


Feedback dispatch
==================

When the first token is `feedback`, read `fn/feedback.md` and run it inline.
This orchestrator handles feedback directly; no fix is attempted on the spot.
Three sub-modes:

```
- capture "<text>": infer the target sub-skill (cross-cutting guard first, then
    keyword in text, else active stage from .intervention-console.yaml, else the
    orchestrator fallback), write one dated file into THAT skill's feedback/
    folder (create it + README lazily if missing), then confirm where it landed
    + how it matched.
- feedback list [skill]: aggregate open items across ALL feedback/ inboxes under
    the application skill root (`find <root> -type d -name feedback`, grep
    `status: open`), grouped by skill; [skill] restricts to one inbox.
- feedback move <file> <skill>: re-route a mis-filed item to the right skill's
    feedback/ folder.
```

Else if the first positional is `digest` (target=digest): read `fn/digest.md`
and run it inline. RESOLVE the target session FIRST: no arg = the CURRENT session;
`"<session-name|id>"` = a PAST session -- locate its transcript .jsonl in this
repo's `~/.claude/projects` dir (id directly, or grep the store for the
/rename'd name) and extract its human turns as the transcript to scan. Then
digest distills the discrete TOOL/SKILL feedback you gave, dedups it
(merge-or-create), and AFTER a mandatory confirm gate routes each approved item
through the same `fn/feedback.md` capture (in BATCH mode -- no per-item
re-confirm). Honor `--dry-run` (scan + distill + present the candidate list, then
STOP without filing). NEVER auto-files: nothing is written before you confirm.
Best run from a fresh session for clean context.


Boundary with insight
========================

```
application READS  ← insight (always)
application WRITES → insight (ask + iterate file cards)
application TRIGGERS → probe (via ask, for full-claims GAPs)
insight NEVER reads from applications/
```


Reference docs
================

```
ref/intervention-lifecycle.md         stage spine + venue table + maturity
ref/intervention-dashboard.md         derive-from-disk contract
haipipe-application/ref/              shared ref docs
  session-state-schema.md
  gate-persona.md
  attendance-modes.md
  audience-requirements.md
  application-input-contract.md
  data-contract-schema.md
  report-template.md
  delivery-need.md
```


## Feedback

`/haipipe-application feedback "<text>"` captures a complaint / confusion / wish
about THIS skill (one dated file per item, `status: open`) to fix in a later
revision pass. Capture-time routing: the complaint is inferred to the specific
sub-skill it concerns and written into THAT sub-skill's `feedback/` folder (e.g.
a pitch gripe -> `1-lifecycle/haipipe-application-pitch/feedback/`); cross-cutting
or unclassifiable items fall back to the orchestrator's own `feedback/`. The
folder IS the record of which skill it concerns. Capture is MERGE-OR-CREATE: a
same-topic complaint updates the existing inbox file (append a dated recurrence,
preserve prior wording verbatim, reopen if it was fixed) instead of spawning a
duplicate, so inboxes stay self-limiting. `/haipipe-application feedback list
[skill]` aggregates open items across ALL inboxes; `/haipipe-application feedback
move <file> <skill>` re-routes a mis-filed item. This is feedback about the tool,
not the intervention it produces. Route a `feedback` first-token to the feedback
handler before other parsing. Full convention (keyword->skill map + inbox paths):
`fn/feedback.md`; fallback inbox: `feedback/README.md`.

`/haipipe-application digest ["<session-name|id>"] [--dry-run]` is the bulk
harvester: it scans a session's transcript -- the CURRENT one with no argument,
or a named/id'd PAST session (located by id or by grepping this repo's
`~/.claude/projects` store for the /rename'd name, then extracting its human
turns) -- distills the discrete TOOL/SKILL feedback you gave, dedups it, and
AFTER a mandatory confirm gate routes each approved item through the same
`fn/feedback.md` capture (merge-or-create, in BATCH mode). It never auto-files;
`--dry-run` previews the candidate list without filing; best run from a fresh
session for clean context. Route a `digest` first-positional to the digest
handler before other parsing. Full convention: `fn/digest.md`.


## Behavioral Preferences (portable)

ALWAYS read and honor `PREFERENCES.md` in this skill's own folder: git-tracked
global behavioral preferences (e.g. communicate via ASCII diagrams) that survive a
machine change, unlike the machine-local `~/.claude` auto-memory. Global behavioral
prefs are kept in sync across all orchestrators by `/haipipe-paper digest`'s
global-pref fan-out (merge-or-create; one entry per topic).
