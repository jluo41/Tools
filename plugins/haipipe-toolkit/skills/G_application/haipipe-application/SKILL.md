---
name: haipipe-application
description: "Application layer orchestrator (the G_application umbrella). Routes every session-style workflow in the haipipe stack: ask (research question driver, can trigger D_probe) and external creation (message / ui / report) drawing on K/W from E_insight. All kinds share one session skeleton: SESSION_STATE.json + plan-vN.yaml + gate (persona + attendance) + context loader. Use to ask a research question, draft a patient/clinician message, sketch UI, write a stakeholder report. Trigger: ask, question, session, message, ui, sketch, report, briefing, /haipipe-application."
argument-hint: "[kind] [intent...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-application (orchestrator)
==========================================

User-facing entry for every **session-style workflow** in the toolkit.
A session = one user intent, one case file, one closed report.

```
C_task          executes runs                            (code, GPU)
D_probe    claims from runs                         (yaml + verdicts)
E_insight       cross-probe KB                      (D/I/K/W markdown)
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
             reads insights/ + probes/ + tasks/
             CAN trigger /haipipe-probe + /haipipe-task
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
             NEVER writes to insights/, tasks/, probes/
             artifact: applications/<kind>/<...>.md
```

The asymmetry is intentional — `ask` is the only kind that can mutate
the project's KB. External kinds delegate KB work to `ask` and resume
their own draft once `ask` returns.


Where artifacts live
=====================

```
examples/Proj-X/
├── tasks/                                  (C_task)
├── probes/                            (D_probe)
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


Commands
========

```
/haipipe-application                                dashboard (list current applications/)
/haipipe-application ask <question>                 research session (D_probe-allowed)
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
                                        D_probe + C_task

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
Step 1: Parse $ARGUMENTS.
Step 2: Resolve kind → specialist via verb map.
        - First positional matches a kind keyword → use it.
        - No args → dashboard (list current applications/).
        - Natural language → infer kind from keywords; ASK if ambiguous.
Step 3: Validate project root (cwd-inferred or --project).
Step 4: Dispatch: Skill("haipipe-application-<kind>", args="<rest>").
Step 5: Surface specialist tail.
```


Session skeleton (uniform across kinds)
========================================

Every kind specialist runs this skeleton (phases vary by kind):

```
Phase init      Skill("haipipe-application-plan")
                  writes plan-v1.yaml
                  [G-plan SOFT gate via haipipe-application-gate]

Phase mid       per-kind work (run tasks / probes OR draft prose)
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
G_application READS  ←──── D_probe claims (ask kind only)

G_application TRIGGERS ──→ D_probe (ask kind only, sole external trigger)
G_application TRIGGERS ──→ C_task       (ask kind only)
G_application TRIGGERS ──→ haipipe-insight-{data,information,knowledge,wisdom}
                          (ask kind, files KB cards from materialized evidence)

E_insight     NEVER reads from applications/
```

The ask kind is the **only** outside trigger for D_probe.
External kinds never see tasks/ or probes/ directly; they go
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
```

`session-state-schema.md` / `gate-persona.md` / `attendance-modes.md`
are shared by ALL kinds. `audience-requirements.md` and
`application-input-contract.md` are specific to the external kinds
(message / ui / report); the ask kind does not consult them.


Relation to other top-level skills
====================================

```
A_discover    seeds ideas → may suggest research questions for ask
B_project     project umbrella → owns examples/Proj-X/applications/
C_task        runs code → triggered by ask
D_probe  claims → triggered by ask
E_insight     K/W → REQUIRED INPUT for all kinds
F_paper       parallel external artifact (academic-only twin of report)
```

G_application is the **session hub** of the toolkit. Anything
question-driven, anything that produces a closed artifact with a
journey, lives here.
