---
name: haipipe-application
description: "Application layer orchestrator (the G_application umbrella). Routes every session-style workflow in the haipipe stack: ask (research question driver, can trigger D_experiment) and external creation (message / ui / report) drawing on K/W from E_insight. All kinds share one session skeleton: SESSION_STATE.json + plan-vN.yaml + gate (persona + attendance) + context loader. Use to ask a research question, draft a patient/clinician message, sketch UI, write a stakeholder report. Trigger: ask, question, session, message, ui, sketch, report, briefing, /haipipe-application."
argument-hint: [kind] [intent...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-application (orchestrator)
==========================================

User-facing entry for every **session-style workflow** in the toolkit.
A session = one user intent, one case file, one closed report.

```
C_task          executes runs                            (code, GPU)
D_experiment    claims from runs                         (yaml + verdicts)
E_insight       cross-experiment KB                      (D/I/K/W markdown)
F_paper         academic publication                     (paper-*)
G_application   session workflows                ← THIS SKILL FAMILY
                  - ask      (research question driver)
                  - message  (patient / clinician)
                  - ui       (designer / dev)
                  - report   (regulator / executive / partner)
```

All 4 kinds share one session skeleton — only the **artifact** they
produce differs.


Two kinds of session
=====================

Internal kind (research-facing, writes to KB):

```
  ask        question-driven research session
             reads insights/ + experiments/ + tasks/
             CAN trigger /haipipe-experiment + /haipipe-task
             CAN write to insights/ (new D/I/K/W cards)
             artifact: applications/ask/<NN_slug>/report.md
```

External kinds (consumer-facing, KB-readonly):

```
  message    patient / clinician message
  ui         designer / dev UI sketch + spec
  report     regulator / executive / partner report
             
             all 3:
             reads insights/ only (no exp / task access)
             can chain /haipipe-application ask if KB gap blocks the draft
             NEVER writes to insights/, tasks/, experiments/
             artifact: applications/<kind>/<...>.md
```

The asymmetry is intentional — `ask` is the only kind that can mutate
the project's KB. External kinds delegate KB work to `ask` and resume
their own draft once `ask` returns.


Where artifacts live
=====================

A project always has this canonical shape:

```
<PROJECT_ROOT>/
├── data/                                   ← data contract (hand + generated)
│   ├── contract.yaml                       hand-written: required / optional streams
│   ├── available.md                        generated: what subject has at active cut
│   └── gaps.md                             generated: missing -> block / trim
├── tasks/                                  (C_task)
├── experiments/                            (D_experiment)
├── insights/                               (E_insight)
├── paper/                                  (F_paper)
└── applications/                           ← G_application writes here
    ├── ask/<NN>_<slug>/                    ← research sessions
    │   ├── question.md
    │   ├── SESSION_STATE.json
    │   ├── plans/plan-v{N}.yaml
    │   ├── gates/{NN}-G-<phase>.md
    │   ├── invocations.log
    │   └── report.md
    ├── messages/<YYYY-MM-DD>_<audience>_<slug>.md
    ├── ui/<slug>/                          (sketches + annotated mocks)
    └── reports/<YYYY-MM-DD>_<audience>_<slug>.md
```

`<PROJECT_ROOT>` resolves to one of two locations:

**Multi-subject project (default):**
```
examples/<Proj>/                            ← repo-root examples/
```
Use this when the project spans multiple subjects, cohorts, or
benchmarks (e.g., `examples/ProjB-Bench-2-EventGlucose/`).

**Per-subject project (when --individual is given):**
```
<subject_store>/examples/<Proj>/            ← under the subject's folder
  where <subject_store> = _WorkSpace/A-User-Store/UserGroup-<dataset>/Subject-<id>
```
Use this when the project is scoped to one specific individual
(e.g., subject profiling, per-patient case study). The project
lives alongside the subject's data so the entire per-patient
package — data + analyses — stays co-located:

```
_WorkSpace/A-User-Store/UserGroup-<dataset>/Subject-<id>/
├── 1-SourceStore/, 2-RecStore/, manifest.yaml      (data)
└── examples/<Proj>/                                 (analyses for this subject)
    ├── tasks/, insights/, applications/, ...
```

The session skill is layout-agnostic: once `<PROJECT_ROOT>` is
resolved at Step 3 of routing, every internal path is
project-root-relative. The two layouts differ ONLY in where the
project root lives on disk.


Data contract layer
====================

The optional `data/` folder at the project root declares what data
the project needs. Three files:

```
data/contract.yaml      hand-written -- required + optional streams,
                        minimum windows / density, data-cut policy
data/available.md       generated   -- what the active subject store
                        actually has at the active cut
data/gaps.md            generated   -- missing requireds (BLOCK) +
                        missing optionals (TRIM which analyses)
```

`available.md` + `gaps.md` are regenerated at the start of every
ask session by Phase 1 step A1. Never hand-edit them.

Per-subject layout: contract is reusable across subjects (same
`Subject*-Profile/data/contract.yaml`, different subject manifests
satisfy or fail it).
Multi-subject layout: contract applies to the cohort as a whole; the
orchestrator iterates subjects against it.

When the subject store advances to a new data cut (any cadence —
monthly drop, quarterly release, on-demand re-extract, event
trigger), do NOT fork the project folder. Open a NEW session under
`applications/ask/NN_refresh_<cut-tag>/`. The project root is
stable; sessions are dated case files. The active cut is recorded
as `SESSION_STATE.data_cut`; insight cards carry the same tag in
frontmatter so superseded cards stay diffable in git.

Cut tags are opaque strings owned by the subject manifest
(`v2026-04`, `release-3`, `post-recalibration`, etc.) — the
application skill never assumes a date format or cadence.

See `ref/data-contract-schema.md` for the full schema and the
Phase 1 step A1 resolution rules.


Commands
========

```
/haipipe-application                                dashboard (list current applications/)
/haipipe-application ask <question>                 research session (D_experiment-allowed)
/haipipe-application message <intent>               patient / clinician message
/haipipe-application ui <intent>                    UI sketch / spec
/haipipe-application report <intent>                stakeholder report
/haipipe-application "<natural language>"           infer kind, dispatch
```


Specialists
===========

Kind specialists (one per artifact type):

```
haipipe-application-ask        SESSION: research-question driver
                                        can write to insights/, can trigger
                                        D_experiment + C_task

haipipe-application-message    SESSION: message creation (patient/clinician)
                                        KB-readonly
haipipe-application-ui         SESSION: UI sketch (designer/dev)        KB-readonly
haipipe-application-report     SESSION: stakeholder report               KB-readonly
```

Session machinery (shared by ALL kinds — never invoked directly by user):

```
haipipe-application-plan       writes plan-v{N}.yaml for the active session
haipipe-application-gate       phase-transition gate
                                 (persona + attendance + 3-outcome vocab)
haipipe-application-context    per-task context loader
                                 (READY / BLOCKED / SKIP verdicts)
```

Each kind specialist runs its own phase shape, calling
plan / gate / context at each phase boundary. See the kind specialist's
own SKILL.md for its phase list.


Function Verb Map
=================

```
ask, question, research, /ask, "does X hold?"        -> haipipe-application-ask
message, msg, sms, patient note, clinician message   -> haipipe-application-message
ui, sketch, mockup, screen, layout, wireframe        -> haipipe-application-ui
report, stakeholder, briefing, exec, regulator       -> haipipe-application-report
```


Routing Logic
==============

```
Step 1: Parse $ARGUMENTS (kind keyword, --project, --individual, --auto, --persona).

Step 2: Resolve kind → specialist via verb map.
        - First positional matches a kind keyword → use it.
        - No args → dashboard (list current applications/).
        - Natural language → infer kind from keywords; ASK if ambiguous.

Step 3: Resolve PROJECT_ROOT. This is the most-important routing decision.
        Two layouts (see "Where artifacts live"):

        a) Per-subject layout (preferred when --individual is given):
           PROJECT_ROOT = <individual>/examples/<project-name>
           where <individual> is the value of --individual (must be a valid
           path under _WorkSpace/A-User-Store/UserGroup-*/Subject-*/),
           and <project-name> is taken from --project (basename only) or
           derived from the question slug.

        b) Multi-subject layout (default when --individual is absent):
           PROJECT_ROOT = examples/<project-name>
           where <project-name> is --project (basename) or a sensible slug.

        Decision rule:
          if --individual:
              PROJECT_ROOT = <individual>/examples/<project-name>
          else:
              PROJECT_ROOT = examples/<project-name>

        --project MAY be supplied as either a bare name (e.g.
        "Subject26-Profile") or a full path. The skill treats it as a
        bare name when --individual is set; otherwise as a path.

        If PROJECT_ROOT does not exist on disk, scaffold the canonical
        directory shape (tasks/, insights/, applications/, experiments/,
        paper/) before dispatch.

Step 4: Validate the subject store if --individual was given:
        verify <individual>/1-SourceStore/ exists. If not, BLOCK and
        surface to user.

Step 5: Dispatch: Skill("haipipe-application-<kind>", args="<rest>").
        Pass --project-root <PROJECT_ROOT> --subject-store <individual>
        downstream so the specialist does not have to re-resolve.

Step 6: Surface specialist tail.
```


Session skeleton (uniform across kinds)
========================================

Every kind specialist runs this skeleton (phases vary by kind):

```
Phase init      Skill("haipipe-application-plan")
                  writes plan-v1.yaml
                  [G-plan SOFT gate via haipipe-application-gate]

Phase mid       per-kind work (run tasks / experiments OR draft prose)
                  may invoke haipipe-application-context before each task
                  [G-mid SOFT gate]

Phase post      produce artifact (report.md / message / ui / stakeholder report)
                  [G-post gate; severity varies by kind]
```

State of the active session is in `SESSION_STATE.json`. See
`ref/session-state-schema.md`.

Gates use the soft-gate machinery: 3 outcomes (`approve` / `revise
[feedback]` / `done`), 4 persona presets, 3 attendance modes. See
`ref/gate-persona.md` and `ref/attendance-modes.md`.


Boundary with E_insight
========================

```
E_insight                                   G_application
─────────────────────                       ─────────────────────
"what does the project KNOW?"               "what does the project DO with what it knows?"
permanent KB                                per-session case files
D/I/K/W markdown cards                      ask / message / ui / report
filed by insight-data/-information/         driven by application-<kind>
        -knowledge/-wisdom
```

One-way dependencies:

```
G_application READS  ←──── E_insight (always)
G_application READS  ←──── C_task results (ask kind only)
G_application READS  ←──── D_experiment claims (ask kind only)

G_application TRIGGERS ──→ D_experiment (ask kind only, sole external trigger)
G_application TRIGGERS ──→ C_task       (ask kind only)
G_application TRIGGERS ──→ haipipe-insight-{data,information,knowledge,wisdom}
                          (ask kind, files KB cards from materialized evidence)

E_insight     NEVER reads from applications/
```

The ask kind is the **only** outside trigger for D_experiment.
External kinds never see tasks/ or experiments/ directly; they go
through ask if they need new KB material.


Specialist Return Contract
===========================

```
status:    ok | blocked | failed | gap_unresolved | budget
summary:   2-3 sentences (what artifact + which K/W cited / new entries written)
artifacts: [paths created]
next:      suggested follow-up
```


Files owned by this umbrella
=============================

```
SKILL.md                                  (this file)
ref/session-state-schema.md               SESSION_STATE.json fields
ref/gate-persona.md                       4 preset reviewer voices
ref/attendance-modes.md                   attended / timed / unattended
ref/audience-requirements.md              external-kind audience schema
ref/application-input-contract.md         how to load K/W from E_insight
ref/data-contract-schema.md               data/contract.yaml schema +
                                          Phase 1 A1 resolution rules
ref/report-template.md                    DIKW-spine report.md template
                                          enforced by G-report (HARSH)
```

`session-state-schema.md` / `gate-persona.md` / `attendance-modes.md`
are shared by ALL kinds. `audience-requirements.md` and
`application-input-contract.md` are specific to the external kinds
(message / ui / report); the ask kind does not consult them.
`data-contract-schema.md` is consulted by ask at Phase 1 step A1;
external kinds may read the generated `data/available.md` to know
what data backed the K/W cards they cite.


Relation to other top-level skills
====================================

```
A_discover    seeds ideas → may suggest research questions for ask
B_project     project umbrella → owns examples/Proj-X/applications/
C_task        runs code → triggered by ask
D_experiment  claims → triggered by ask
E_insight     K/W → REQUIRED INPUT for all kinds
F_paper       parallel external artifact (academic-only twin of report)
```

G_application is the **session hub** of the toolkit. Anything
question-driven, anything that produces a closed artifact with a
journey, lives here.
